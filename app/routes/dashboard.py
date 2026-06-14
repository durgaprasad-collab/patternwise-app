from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.core.database import SessionLocal
from app.models.birth_profile import BirthProfile
from app.astrology.services.chart_repository import ChartRepository
from app.models.user import User

router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)

@router.get("/dashboard")
async def dashboard(request: Request):
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
    print("DB USER:", db_user.id)
    
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
    print(
    "PROFILE ID:",
    profile.id if profile else None
)

    chart_record = None
    if profile:
        chart_record = ChartRepository.get_latest_chart(
        profile.id
    )
        print(
    "CHART ID:",
    chart_record.id if chart_record else None
)
        print("\nCOSMIC PROFILE SENT TO TEMPLATE")
        print(chart_record.profile_json)
        print("===============================\n")
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
   

   