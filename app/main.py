import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.admin import init_admin
from app.api.webhook import router
from app.db.session import init_db, async_engine

logger.remove()
logger.add(
	sys.stdout,
	format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>",
	level="INFO"
)
logger.add(
	"logs/app_{time}.log",
	rotation="500 MB",
	retention="10 days",
	level="DEBUG"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
	"""Gerenciador de contexto para o ciclo de vida da aplicação FastAPI."""
	logger.info(f"🚀 Iniciando aplicação")

	logger.info("🔄 Inicializando banco de dados...")
	await init_db()
	logger.info("✅ Banco de dados inicializado com sucesso.")

	yield
	logger.info("🛑 Finalizando aplicação")


app = FastAPI(
	title="NF Bot Zap Extractor With IA",
	version="1.0.0",
	description="API para integração com o ChatBot WhatsApp extração de NF via IA",
	lifespan=lifespan,
	docs_url="/docs",
	redoc_url="/redoc",
	root_path="/api/v1"
)

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

init_admin(app, async_engine)
app.include_router(router, prefix="/evolution", tags=["Webhook Evolution"])

if __name__ == "__main__":
	import uvicorn

	uvicorn.run(
		"app.main:app",
		host="0.0.0.0",
		port=8000,
		reload=True,
		log_level="info",
		env_file=".env",
	)
