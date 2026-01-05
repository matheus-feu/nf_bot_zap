from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, field_validator


class ItemNoteBase(BaseModel):
	product_name: str
	product_code: Optional[str] = None
	ncm: Optional[str] = None
	cfop: Optional[str] = None
	discount_value: Optional[Decimal] = None
	icms_value: Optional[Decimal] = None
	ipi_value: Optional[Decimal] = None
	quantity: Optional[Decimal] = None
	unit_of_measure: Optional[str] = None
	unit_value: Optional[Decimal] = None


class ItemNoteCreate(ItemNoteBase):
	note_id: int


class ItemNoteRead(ItemNoteBase):
	id: int
	created_at: datetime

	model_config = ConfigDict(from_attributes=True)


class NoteBase(BaseModel):
	note_type: Optional[str] = None
	note_number: Optional[str] = None
	series: Optional[str] = None
	access_key: Optional[str] = None
	issuer_cnpj: Optional[str] = None
	issuer_ie: Optional[str] = None
	issuer_city: Optional[str] = None
	issuer_state: Optional[str] = None
	issuer_zip_code: Optional[str] = None
	provider: str
	nature_of_operation: Optional[str] = None
	protocol_number: Optional[str] = None
	date_of_issue: date
	total_value: Decimal
	pdf_url: Optional[str] = None

	@field_validator("date_of_issue", mode="before")
	@classmethod
	def parse_br_or_iso_date(cls, v):
		if isinstance(v, date):
			return v
		if isinstance(v, str):
			for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
				try:
					return datetime.strptime(v, fmt).date()
				except ValueError:
					continue
		raise ValueError("Formato de data inválido")


class NoteCreate(NoteBase):
	items: List[ItemNoteBase]


class NoteRead(NoteBase):
	id: int
	created_at: datetime
	items: List[ItemNoteRead] = []

	model_config = ConfigDict(from_attributes=True)
