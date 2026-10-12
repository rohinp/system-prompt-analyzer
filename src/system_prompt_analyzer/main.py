from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .analyzer import analyze_prompt
from .config import get_settings
from .rubric import rubric_response
from .schemas import AnalyzeRequest, AnalyzeResponse, RubricResponse, RuntimeConfigResponse

PACKAGE_DIR = Path(__file__).parent


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title=settings.app_name,
        description="Visual analysis of system-prompt rules, constraints, guards, and gaps.",
        version="0.1.0",
    )
    application.mount("/static", StaticFiles(directory=PACKAGE_DIR / "static"), name="static")
    templates = Jinja2Templates(directory=PACKAGE_DIR / "templates")

    @application.get("/", response_class=HTMLResponse, include_in_schema=False)
    async def index(request: Request) -> HTMLResponse:
        return templates.TemplateResponse(request=request, name="index.html")

    @application.get("/api/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @application.get("/api/config", response_model=RuntimeConfigResponse)
    async def runtime_config() -> RuntimeConfigResponse:
        return RuntimeConfigResponse(
            provider=settings.model_provider,
            model=settings.model_name,
            api_key_configured=bool(settings.model_api_key),
        )

    @application.get("/api/rubric", response_model=RubricResponse)
    async def rubric() -> RubricResponse:
        return rubric_response()

    @application.post("/api/analyze", response_model=AnalyzeResponse)
    async def analyze(payload: AnalyzeRequest) -> AnalyzeResponse:
        return analyze_prompt(payload.prompt)

    return application


app = create_app()


def run() -> None:
    settings = get_settings()
    uvicorn.run(
        "system_prompt_analyzer.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_env == "development",
    )
