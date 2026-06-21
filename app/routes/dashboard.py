from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.core.database import SessionLocal
from app.models.birth_profile import BirthProfile
from app.models.user import User
from app.astrology.services.chart_repository import ChartRepository

router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/dashboard")
async def dashboard(request: Request):

    db = SessionLocal()

    try:

        user = request.session.get("user")

        if not user:
            return RedirectResponse(
                "/login",
                status_code=303
            )

        db_user = (
            db.query(User)
            .filter(
                User.email == user["email"]
            )
            .first()
        )

        if not db_user:
            return RedirectResponse(
                "/login",
                status_code=303
            )

        profile = (
            db.query(BirthProfile)
            .filter(
                BirthProfile.user_id == db_user.id
            )
            .first()
        )

        if not profile:

            return RedirectResponse(
                url="/onboarding/birth-profile",
                status_code=303
            )

        chart_record = ChartRepository.get_latest_chart(
            profile.id
        )

        return templates.TemplateResponse(
            request=request,
            name="pages/dashboard.html",
            context={
                "request": request,
                "user": user,
                "profile": profile,
                "chart": (
                    chart_record.chart_json
                    if chart_record
                    else None
                ),
                "cosmic_profile": (
                    chart_record.profile_json
                    if chart_record
                    else None
                )
            }
        )

    finally:
        db.close()
