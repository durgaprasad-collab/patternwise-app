from urllib.parse import urlparse

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.routes.auth import router as auth_router
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from app.routes.dashboard import router as dashboard_router
from app.core.config import settings
from app.routes.onboarding import router as onboarding_router
from app.routes.profile import router as profile_router
app = FastAPI()

app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(onboarding_router)
app.include_router(profile_router)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET,
    https_only=settings.is_production,
    same_site="lax",
    max_age=60 * 60 * 24 * 14,
)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.allowed_hosts,
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.middleware("http")
async def security_middleware(request: Request, call_next):
    if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
        origin = request.headers.get("origin")
        if origin:
            origin_host = urlparse(origin).netloc
            request_host = request.headers.get("host", "")
            if origin_host != request_host:
                return JSONResponse(
                    {"detail": "Invalid request origin"},
                    status_code=403,
                )

    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = (
        "camera=(), microphone=(), geolocation=()"
    )
    if settings.is_production:
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
    return response


@app.get("/health", include_in_schema=False)
async def health():
    return {"status": "ok"}


@app.get("/")
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )

@app.get("/about")
async def about(request: Request):

    if request.headers.get("HX-Request"):

        return templates.TemplateResponse(
            request=request,
            name="pages/about_content.html",
            context={}
        )

    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context={
            "request": request
        }
    )
