from datetime import datetime, timezone, timedelta

from fastapi import Request, BackgroundTasks
from fastapi.params import Depends
from fastapi.routing import APIRouter
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.services.evolution.evolution_integration import evolution_client
from app.services.notes_service import process_pdf_b64

router = APIRouter()


@router.post("/webhook")
async def evolution_webhook(
		request: Request,
		background_tasks: BackgroundTasks,
		db: AsyncSession = Depends(get_db_session)
):
	"""Endpoint to receive webhook events from Evolution API."""
	raw = await request.json()
	logger.info(f"📥 Webhook bruto recebido: {raw}")

	if raw.get("event") != "messages.upsert":
		return {"message": "ignored"}

	data = raw.get("data") or {}
	key = data.get("key") or {}
	message = data.get("message") or {}

	remote_jid = key.get("remoteJid")
	if not remote_jid:
		return {"message": "missing remoteJid"}

	phone_number = remote_jid.split("@", 1)[0]

	document = message.get("documentMessage")
	if not document:
		return {"message": "ignored: not document"}

	msg_ts = data.messageTimestamp
	msg_time = datetime.fromtimestamp(int(msg_ts), tz=timezone.utc)
	now = datetime.now(timezone.utc)
	if now - msg_time > timedelta(minutes=2):
		return {"message": "Mensagem muito antiga ignorada"}

	mimetype = document.get("mimetype")
	file_name = document.get("fileName") or document.get("title") or ""

	if mimetype != "application/pdf" or not file_name.lower().endswith(".pdf"):
		background_tasks.add_task(
			evolution_client.send_text_message,
			phone_number,
			"Só aceito arquivos PDF de nota fiscal para registro. Envie um PDF válido.",
		)
		return {"message": "invalid mimetype"}

	url = document.get("url")
	if not url:
		return {"message": "missing document url"}

	title = document.get("title") or file_name
	message_id = key.get("id")

	async def process():
		try:
			pdf_b64 = await evolution_client.get_base64_from_media_message(message_id)
			await process_pdf_b64(pdf_b64, db, pdf_url=url)
			await evolution_client.send_text_message(
				phone_number,
				f"Nota fiscal '{title}' processada com sucesso e registrada no sistema.",
			)
		except Exception as e:
			logger.exception(f"Erro ao processar nota fiscal: {e}")
			await evolution_client.send_text_message(
				phone_number,
				"Tive um erro ao processar sua nota fiscal. Tente novamente em alguns minutos.",
			)

	background_tasks.add_task(process)
	return {"message": "PDF received, processing started"}
