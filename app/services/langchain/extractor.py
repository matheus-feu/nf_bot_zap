import json
from typing import Any, Dict

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from loguru import logger

from app.core.config import settings
from app.services.langchain.prompts import NF_PDF_EXTRACT_PROMPT


class NFExtractor:
	def __init__(self, model_name: str = "gemini-2.0-flash") -> None:
		self._model = ChatGoogleGenerativeAI(
			model=model_name,
			api_key=settings.google_api_key,
		)

	async def _extract_json_string(self, raw: str) -> str:
		start = raw.find("{")
		end = raw.rfind("}")
		if start == -1 or end == -1 or end <= start:
			raise ValueError(f"No JSON object found in model output: {raw!r}")
		return raw[start:end + 1]

	async def extract_from_b64(self, pdf_b64: str) -> Dict[str, Any]:
		if isinstance(pdf_b64, bytes):
			pdf_b64 = pdf_b64.decode("utf-8")

		message = HumanMessage(
			content=[
				{"type": "text", "text": NF_PDF_EXTRACT_PROMPT},
				{
					"type": "file",
					"mime_type": "application/pdf",
					"base64": pdf_b64,
				},
			]
		)

		resp = await self._model.ainvoke([message])
		raw = resp.content

		if isinstance(raw, list):
			raw = "".join(
				part["text"]
				for part in raw
				if isinstance(part, dict) and "text" in part
			)

		json_str = await self._extract_json_string(raw)
		return json.loads(json_str)


nf_extractor: NFExtractor = NFExtractor()
