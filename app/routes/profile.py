from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.astrology.services import chart_service
from app.core.database import SessionLocal, get_db
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.birth_profile_repository import (
    BirthProfileRepository
)

router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/profile")
async def profile_page(request: Request):
    db = SessionLocal()

    user = request.session.get("user")

    if not user:
        return RedirectResponse("/login")

    db_user = (
        db.query(User)
        .filter(
            User.email == user["email"]
        )
        .first()
    )

    profile = (
        BirthProfileRepository.get_by_user_id(
            db,
            db_user.id
        )
    )
    print("SESSION USER =", user)
    print("DB USER FULL NAME =", db_user.full_name)
    return templates.TemplateResponse(
        request=request,
        name="pages/profile.html",
        context={
            "request": request,
            "user": user,
            "db_user": db_user,
            "profile": profile
        }
    )

@router.get("/profile/edit")
async def edit_profile_page(
    request: Request,
    db: Session = Depends(get_db)
):
    user_session = request.session.get("user")

    if not user_session:
        return RedirectResponse("/", status_code=302)

    user = (
    db.query(User)
    .filter(User.email == user_session["email"])
    .first()
)

    profile = BirthProfileRepository.get_by_user_id(
    db,
    user.id
)

    return templates.TemplateResponse(
        "pages/edit_profile.html",
        {
            "request": request,
            "user": user_session,
            "profile": profile
        }
    )
@router.post("/profile/edit")
async def update_profile(
    request: Request,
    birth_date: str,
    birth_time: str,
    location_name: str,
    db: Session = Depends(get_db)
):

    user_session = request.session.get("user")

    if not user_session:
        return RedirectResponse("/", status_code=302)

    user = (
    db.query(User)
    .filter(User.email == user_session["email"])
    .first()
)

    profile = BirthProfileRepository.get_by_user_id(
        db,
        user.id
    )

    if profile:
        profile.birth_date = birth_date
        profile.birth_time = birth_time
        profile.location_name = location_name
        db.commit()
        db.refresh(profile)
        chart_service = chart_service.ChartServicee.ChartService(db)
        chart_service.generate_and_save_chart(
    profile.id
)
    return RedirectResponse("/dashboard", status_code=302)