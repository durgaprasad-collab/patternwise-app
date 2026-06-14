from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.routes.auth import router as auth_router
from starlette.middleware.sessions import SessionMiddleware
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
    secret_key=settings.SESSION_SECRET
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


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