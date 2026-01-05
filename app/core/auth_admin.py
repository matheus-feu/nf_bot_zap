from fastapi import Request
from sqladmin.authentication import AuthenticationBackend

from app.core.config import settings


class AdminAuth(AuthenticationBackend):
	async def login(self, request: Request) -> bool:
		form = await request.form()
		username, password = form.get("username"), form.get("password")

		if username != settings.admin_username or password != settings.admin_password:
			return False

		request.session.update({"admin_token": "ok"})
		return True

	async def logout(self, request: Request) -> bool:
		request.session.clear()
		return True

	async def authenticate(self, request: Request) -> bool:
		token = request.session.get("admin_token")
		if not token:
			return False
		return True
