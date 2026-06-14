import profile

from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.location.geocoder import search_city
from app.services.location.timezone import get_timezone
from datetime import datetime

from app.core.database import SessionLocal
from app.models.birth_profile import BirthProfile
from app.astrology.services.chart_service import ChartService

router = APIRouter()

templates = Jinja2Templates(
directory="app/templates"
)

@router.get("/onboarding/birth-profile")
async def birth_profile_page(request: Request):

    user = request.session.get("user")

    if not user:
        return RedirectResponse(
        url="/login",
        status_code=302
    )

    return templates.TemplateResponse(
    request=request,
    name="pages/onboarding/birth_profile.html",
    context={
        "request": request,
        "user": user
    }
)


@router.post("/onboarding/birth-date")
async def birth_date_step(
request: Request,
birth_date: str = Form(...)
):
    request.session["birth_date"] = birth_date

    return templates.TemplateResponse(
    request=request,
    name="pages/onboarding/steps/step_birth_time.html",
    context={
        "request": request
    }
)

@router.post("/onboarding/birth-time")
async def birth_time_step(
request: Request,
birth_time: str = Form(...)
):


    request.session["birth_time"] = birth_time

    return templates.TemplateResponse(
    request=request,
    name="pages/onboarding/steps/step_birth_location.html",
    context={
        "request": request
    }
)


@router.get("/onboarding/location-search")
async def location_search(
    request: Request,
    query: str = "",
    location: str = ""
):

    search_text = query or location

    print("QUERY:", search_text)

    results = search_city(search_text)

    return templates.TemplateResponse(
        request=request,
        name="pages/onboarding/steps/location_results.html",
        context={
            "request": request,
            "results": results
        }
    )


@router.post("/onboarding/select-location")
async def select_location(
    request: Request,
    location_name: str = Form(...),
    latitude: str = Form(...),
    longitude: str = Form(...)
):
    timezone_name = get_timezone(latitude, longitude)

    request.session["location"] = {
        "name": location_name,
        "latitude": latitude,
        "longitude": longitude,
        "timezone": timezone_name,
    }

    print("\nLOCATION SAVED:")
    print(request.session["location"])

    return templates.TemplateResponse(
        request=request,
        name="pages/onboarding/steps/review_profile.html",
        context={
            "request": request,
            "birth_date": request.session.get("birth_date"),
            "birth_time": request.session.get("birth_time"),
            "location": request.session.get("location"),
        },
    )

@router.get("/onboarding/review")
async def review_profile(request: Request):

    print("\nSESSION DATA:")
    print(request.session)

    return templates.TemplateResponse(
    request=request,
    name="pages/onboarding/steps/review_profile.html",
    context={
        "request": request,
        "birth_date": request.session.get("birth_date"),
        "birth_time": request.session.get("birth_time"),
        "location": request.session.get("location")
    }
)


@router.post("/onboarding/save-profile")
async def save_profile(request: Request):

    db = SessionLocal()

    try:

        user_id = request.session.get("user_id")

        print("SESSION USER ID:", user_id)

        if not user_id:
            return RedirectResponse(
                url="/login",
                status_code=303
            )

        location = request.session.get("location")
        existing_profile = (
            db.query(BirthProfile)
            .filter(BirthProfile.user_id == user_id)
            .first()
        )
        print("USER ID:", user_id)
        print("EXISTING PROFILE:", existing_profile)
        if existing_profile:
            existing_profile.birth_date =datetime.strptime(request.session.get("birth_date"), "%Y-%m-%d").date()
            existing_profile.birth_time = datetime.strptime(request.session.get("birth_time"), "%H:%M").time()
            existing_profile.location_name = location["name"]
            existing_profile.latitude = location["latitude"]
            existing_profile.longitude = location["longitude"]
            existing_profile.timezone = location["timezone"]

            profile = existing_profile
            print ("UPDATING EXISTING PROFILE:", profile.id)
        else:
            profile = BirthProfile(
                user_id=user_id,
                birth_date=datetime.strptime(request.session.get("birth_date"), "%Y-%m-%d").date(),
                birth_time=datetime.strptime(request.session.get("birth_time"), "%H:%M").time(),
                location_name=location["name"],
                latitude=location["latitude"],
                longitude=location["longitude"],
                timezone=location["timezone"]
            )
            db.add(profile)
            print("CREATING NEW PROFILE")
        db.commit()
        db.refresh(profile)

        print("PROFILE SAVED OK")
        print("PROFILE ID:", profile.id)
        print("BIRTH DATE:", profile.birth_date)
        print("BIRTH TIME:", profile.birth_time)
        generated_chart = (
           ChartService.generate_and_save_chart(
               profile.id
           )
        )
        print(
           "GENERATED CHART:",
            generated_chart.id
        )
      
        return HTMLResponse("""
        <div class="p-8 text-center">
            <h2 class="text-2xl font-bold text-green-500">
                Birth Profile Saved Successfully
            </h2>

            <p class="mt-4 text-gray-300">
                Your birth information has been stored in PatternWise.
            </p>

            <div class="mt-6">
                <a
                    href="/dashboard"
                    class="px-6 py-3 rounded-lg bg-indigo-600 text-white hover:bg-indigo-500"
                >
                    Return to Dashboard
                </a>
            </div>
        </div>
        """)

    except Exception as e:

        db.rollback()

        print("SAVE ERROR:", str(e))

        return HTMLResponse(
            f"<h2>Database Error</h2><pre>{str(e)}</pre>",
            status_code=500
        )

    finally:
        db.close()
    