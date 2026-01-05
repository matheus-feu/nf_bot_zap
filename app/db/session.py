from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.core.config import settings
from app.db.base import Base

async_engine = create_async_engine(settings.sqlalchemy_database_uri, future=True)

AsyncSessionLocal = async_sessionmaker(
	async_engine,
	class_=AsyncSession,
	expire_on_commit=False,
	autocommit=False,
	autoflush=False
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
	"""
	Dependency que fornece sessão do banco.
	Uso: db: AsyncSession = Depends(get_db_session)
	"""
	async with AsyncSessionLocal() as session:
		try:
			yield session
		finally:
			await session.close()


async def init_db():
	"""Inicializa o banco de dados (cria tabelas se necessário)."""
	import app.models  # noqa: F401

	async with async_engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)
