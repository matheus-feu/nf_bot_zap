from typing import Any, Dict, List, Optional

import httpx
from loguru import logger

from app.core.config import settings


class EvolutionIntegration:
	"""
	Client to interact with the Evolution API.
	https://doc.evolution-api.com/v2/pt/get-started/introduction
	"""

	def __init__(self):
		self.base_url = settings.evolution_api_url
		self.api_key = settings.authentication_api_key
		self.instance_name = settings.evolution_instance_name
		self.headers = {
			"apikey": self.api_key,
			"Content-Type": "application/json",
		}
		self._client = httpx.AsyncClient(timeout=20.0)

	async def close(self):
		await self._client.aclose()

	async def _post(self, path: str, json: Dict[str, Any]) -> Dict[str, Any]:
		url = f"{self.base_url}{path}/{self.instance_name}"

		try:
			resp = await self._client.post(url, headers=self.headers, json=json)
			resp.raise_for_status()
			return resp.json()

		except httpx.HTTPStatusError as exc:
			logger.error(
				"[Evolution] HTTP error %s for %s payload=%s body=%s",
				exc.response.status_code,
				url,
				json,
				exc.response.text,
			)
			raise

		except httpx.RequestError as exc:
			logger.error(
				"[Evolution] Request error for %s payload=%s detail=%s",
				url,
				json,
				str(exc),
			)
			raise

	async def get_base64_from_media_message(self, message_id: str) -> str:
		"""
		Gets the base64 representation of a media message by its ID.
		:param message_id:
		:return:
		"""
		payload = {
			"message": {"key": {"id": message_id}},
			"convertToMp4": False,
		}
		resp = await self._post("/chat/getBase64FromMediaMessage", payload)
		return resp.get("base64", "")

	async def send_text_message(self, phone_number: str, message: str) -> dict:
		"""
		Sends a text message to the specified phone number via the Evolution API.
		:param phone_number:
		:param message:
		:return:
		"""
		payload: dict = {
			"number": phone_number,
			"text": message,
			"delay": 1000,
		}
		return await self._post("/message/sendText", payload)

	async def send_media_url_message(
			self,
			phone_number: str,
			media_url: str,
			caption: str = ""
	) -> dict:
		"""
		Sends a media message (image) to the specified phone number via the Evolution API.
		:param phone_number:
		:param media_url:
		:param caption:
		:return:
		"""
		payload: dict = {
			"number": phone_number,
			"mediatype": "image",
			"mimetype": "image/png",
			"caption": caption,
			"media": media_url,
			"fileName": "image.jpg",
			"delay": 1200,
		}
		return await self._post("/message/sendMedia", payload)

	async def send_button_message(
			self,
			phone_number: str,
			title: str,
			description: str,
			buttons: list[tuple[str, str]]
	) -> dict:
		"""
		Sends a button message to the specified phone number via the Evolution API.
		:param phone_number:
		:param title:
		:param description:
		:param buttons: List of tuples containing button text and button ID
		:return:
		"""
		payload = {
			"number": phone_number,
			"title": title,
			"description": description,
			"footer": "Selecione uma opção",
			"buttons": [
				{
					"type": "reply",
					"displayText": btn_text,
					"id": btn_id,
				}
				for btn_text, btn_id in buttons
			],
		}
		return await self._post("/message/sendButtons", payload)

	async def send_list_message(
			self,
			phone_number: str,
			title: str,
			description: str,
			button_text: str,
			sections: List[Dict[str, Any]],
			footer_text: str | None = None,
			delay: int | None = None,
	) -> dict:
		"""
		sections:
		[
		  {
			"title": "Row title 01",
			"rows": [
			  {"title": "Title row 01", "description": "...", "rowId": "rowId 001"},
			  {"title": "Title row 02", "description": "...", "rowId": "rowId 002"},
			],
		  },
		  ...
		]
		"""
		payload: Dict[str, Any] = {
			"number": phone_number,
			"title": title,
			"description": description,
			"buttonText": button_text,
			"sections": sections,
		}
		if footer_text:
			payload["footerText"] = footer_text
		if delay is not None:
			payload["delay"] = delay

		return await self._post("/message/sendList", payload)

	async def send_sticker_message(
			self,
			phone_number: str,
			sticker_url_or_base64: str,
			delay: Optional[int] = None,
			quoted_id: Optional[str] = None,
	) -> dict:
		"""
		Envia um sticker para o número informado.
		`sticker_url_or_base64` pode ser uma URL pública ou um base64 suportado pela Evolution.
		"""
		payload: Dict[str, Any] = {
			"number": phone_number,
			"sticker": sticker_url_or_base64,
		}

		if delay is not None:
			payload["delay"] = delay

		if quoted_id:
			payload["quoted"] = {
				"key": {"id": quoted_id},
			}
		return await self._post("/message/sendSticker", payload)

	async def send_poll_message(
			self,
			phone_number: str,
			question: str,
			values: List[str],
			selectable_count: int = 1,
			delay: Optional[int] = None,
	) -> dict:
		"""
		Envia uma mensagem de enquete (poll) para o número informado.
		`values` deve ser uma lista de strings, cada uma representando uma opção.
		"""
		payload: Dict[str, Any] = {
			"number": phone_number,
			"name": question,
			"selectableCount": selectable_count,
			"values": values,
		}

		if delay is not None:
			payload["delay"] = delay

		return await self._post("/message/sendPoll", payload)

	async def send_location_message(
			self,
			phone_number: str,
			name: str,
			address: str,
			latitude: float,
			longitude: float,
			delay: Optional[int] = None,
			quoted_id: Optional[str] = None,
	) -> dict:
		"""
		Envia uma mensagem de localização para o número informado.
		"""
		payload: Dict[str, Any] = {
			"number": phone_number,
			"name": name,
			"address": address,
			"latitude": latitude,
			"longitude": longitude,
		}

		if delay is not None:
			payload["delay"] = delay

		if quoted_id:
			payload["quoted"] = {
				"key": {"id": quoted_id},
			}

		return await self._post("/message/sendLocation", payload)

	async def send_narrated_audio_message(
			self,
			phone_number: str,
			audio_url_or_base64: str,
			delay: Optional[int] = None,
			quoted_id: Optional[str] = None,
			mentions_everyone: bool = False,
			mentioned: Optional[List[str]] = None,
			encoding: bool = True,
	) -> dict:
		"""
		Envia um áudio narrado para o número informado.
		`audio_url_or_base64` pode ser URL pública ou base64 suportado.
		"""
		payload: Dict[str, Any] = {
			"number": phone_number,
			"audio": audio_url_or_base64,
			"encoding": encoding,
		}

		if delay is not None:
			payload["delay"] = delay

		if quoted_id:
			payload["quoted"] = {
				"key": {"id": quoted_id},
			}

		if mentions_everyone:
			payload["mentionsEveryOne"] = True

		if mentioned:
			payload["mentioned"] = mentioned

		return await self._post("/message/sendWhatsAppAudio", payload)


evolution_client: EvolutionIntegration = EvolutionIntegration()
