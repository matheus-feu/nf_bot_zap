from sqladmin import Admin

from app.admin.notes import NoteAdmin, ItemNoteAdmin
from app.core.auth_admin import AdminAuth
from app.core.config import settings


def init_admin(app, engine) -> None:
	"""Inicializa o painel administrativo."""

	authentication_backend = AdminAuth(secret_key=settings.secret_key)
	admin = Admin(
		app,
		engine,
		base_url="/admin",
		title="Painel Administrativo",
		authentication_backend=authentication_backend
	)
	admin.add_view(NoteAdmin)
	admin.add_view(ItemNoteAdmin)
