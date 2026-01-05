from functools import lru_cache
from urllib.parse import urlsplit, urlunsplit

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	project_name: str = "nf-bot-zap"
	api_v1_str: str = "/api/v1"

	database_connection_uri: str

	cache_redis_uri: str

	evolution_api_url: str
	authentication_api_key: str
	evolution_instance_name: str

	google_api_key: str

	admin_username: str
	admin_password: str
	secret_key: str

	@property
	def sqlalchemy_database_uri(self) -> str:
		"""
		Generates a SQLAlchemy-compatible database connection URI using the asyncpg driver.
		:return: A database connection URI formatted for SQLAlchemy with asyncpg driver.
		"""
		raw = self.database_connection_uri
		raw = raw.replace("postgresql://", "postgresql+asyncpg://", 1)
		parts = urlsplit(raw)

		if not parts.path:
			raise ValueError("DATABASE_CONNECTION_URI precisa ter o nome do banco no path")

		cleaned = urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))
		return cleaned

	model_config = SettingsConfigDict(
		env_file=".env",
		env_file_encoding="utf-8",
		extra="ignore",
		json_schema_extra={'enable_decoding': False}
	)


@lru_cache()
def get_settings() -> Settings:
	return Settings()


settings = get_settings()
