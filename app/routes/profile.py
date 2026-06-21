from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.core.database import SessionLocal
from app.models.user import User
from app.repositories.birth_profile_repository import BirthProfileRepository


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/profile")
async def profile_page(request: Request):
    user_session = request.session.get("user")
    if not user_session:
        return RedirectResponse("/login", status_code=303)

    db = SessionLocal()
    try:
        db_user = (
            db.query(User)
            .filter(User.email == user_session["email"])
            .first()
        )
        if not db_user:
            request.session.clear()
            return RedirectResponse("/login", status_code=303)

        profile = BirthProfileRepository.get_by_user_id(db, db_user.id)
        if not profile:
            return RedirectResponse(
                "/onboarding/birth-profile",
                status_code=303,
            )

        return templates.TemplateResponse(
            request=request,
            name="pages/profile.html",
            context={
                "request": request,
                "user": user_session,
                "db_user": db_user,
                "profile": profile,
            },
        )
    finally:
        db.close()


@router.get("/profile/edit")
async def edit_profile_page(request: Request):
    if not request.session.get("user"):
        return RedirectResponse("/login", status_code=303)
    return RedirectResponse(
        "/onboarding/birth-profile",
        status_code=303,
    )
