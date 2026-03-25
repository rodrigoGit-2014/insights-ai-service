from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.exceptions import validation_exception_handler, sqlalchemy_exception_handler, general_exception_handler
from app.api.v1.router import api_router

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

@app.on_event("startup")
async def startup_event():
    from app.db.session import create_tables
    create_tables()
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")

@app.get("/", status_code=status.HTTP_200_OK, tags=["Health"])
def root():
    return {"message": f"Welcome to {settings.APP_NAME}", "version": settings.APP_VERSION}

@app.get("/health", status_code=status.HTTP_200_OK, tags=["Health"])
def health():
    return {"status": "healthy", "service": settings.APP_NAME, "version": settings.APP_VERSION}
