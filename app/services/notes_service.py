import time

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notes import Note, ItemNote
from app.schemas.notes import NoteCreate, ItemNoteBase
from app.services.langchain.extractor import nf_extractor


async def process_pdf_b64(pdf_b64: str, db: AsyncSession, pdf_url: str | None = None) -> None:
	t0 = time.perf_counter()
	nf_dict = await nf_extractor.extract_from_b64(pdf_b64)
	logger.info(nf_dict)
	t1 = time.perf_counter()
	logger.info(f"extract_from_b64 levou {t1 - t0:.2f}s")

	raw_items = nf_dict.get("items") or []
	valid_items = [
		i for i in raw_items
		if i.get("product_name")
		   and i.get("quantity") is not None
		   and i.get("unit_of_measure")
		   and i.get("unit_value") is not None
	]

	note_in = NoteCreate(
		note_type=nf_dict.get("note_type"),
		note_number=nf_dict.get("note_number"),
		series=nf_dict.get("series"),
		access_key=nf_dict.get("access_key"),
		issuer_cnpj=nf_dict.get("issuer_cnpj"),
		issuer_ie=nf_dict.get("issuer_ie"),
		issuer_city=nf_dict.get("issuer_city"),
		issuer_state=nf_dict.get("issuer_state"),
		issuer_zip_code=nf_dict.get("issuer_zip_code"),
		provider=nf_dict["provider"],
		nature_of_operation=nf_dict.get("nature_of_operation"),
		protocol_number=nf_dict.get("protocol_number"),
		date_of_issue=nf_dict["date_of_issue"],
		total_value=nf_dict["total_value"],
		pdf_url=pdf_url or "",
		items=[
			ItemNoteBase(
				product_name=i["product_name"],
				product_code=i.get("product_code"),
				ncm=i.get("ncm"),
				cfop=i.get("cfop"),
				discount_value=i.get("discount_value"),
				icms_value=i.get("icms_value"),
				ipi_value=i.get("ipi_value"),
				quantity=i.get("quantity"),
				unit_of_measure=i.get("unit_of_measure"),
				unit_value=i.get("unit_value"),
			)
			for i in valid_items
		],
	)

	note = Note(
		note_type=note_in.note_type,
		note_number=note_in.note_number,
		series=note_in.series,
		access_key=note_in.access_key,
		issuer_cnpj=note_in.issuer_cnpj,
		issuer_ie=note_in.issuer_ie,
		issuer_city=note_in.issuer_city,
		issuer_state=note_in.issuer_state,
		issuer_zip_code=note_in.issuer_zip_code,
		provider=note_in.provider,
		nature_of_operation=note_in.nature_of_operation,
		protocol_number=note_in.protocol_number,
		date_of_issue=note_in.date_of_issue,
		total_value=note_in.total_value,
		pdf_url=note_in.pdf_url,
	)
	db.add(note)
	await db.flush()

	for item_in in note_in.items:
		db.add(
			ItemNote(
				note_id=note.id,
				product_name=item_in.product_name,
				product_code=item_in.product_code,
				ncm=item_in.ncm,
				cfop=item_in.cfop,
				discount_value=item_in.discount_value,
				icms_value=item_in.icms_value,
				ipi_value=item_in.ipi_value,
				quantity=item_in.quantity,
				unit_of_measure=item_in.unit_of_measure,
				unit_value=item_in.unit_value,
			)
		)

	await db.commit()
