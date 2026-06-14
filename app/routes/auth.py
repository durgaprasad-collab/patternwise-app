from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuthError
from httpx import request
from app.auth.oauth import oauth
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.user import User

templates = Jinja2Templates(
    directory="app/templates"
)
router = APIRouter()


@router.get("/login")
async def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "request": request
        }
    )



@router.get("/logout")
async def logout(request: Request):

    request.session.clear()

    return RedirectResponse(
        url="/",
        status_code=303
    )

@router.get("/login/google")
async def login_google(request: Request):

    redirect_uri = request.url_for("auth_callback")

    print("REDIRECT URI:", redirect_uri)

    return await oauth.google.authorize_redirect(
        request,
        redirect_uri
    )

@router.get("/auth/callback")
async def auth_callback(request: Request):

    try:

        token = await oauth.google.authorize_access_token(
            request
        )

        print("TOKEN RECEIVED")
        print(token)

        google_user = token.get("userinfo")

        print("GOOGLE USER")
        print(google_user)

        db: Session = SessionLocal()

        try:

            existing_user = (
                db.query(User)
                .filter(
                    User.email == google_user["email"]
                )
                .first()
            )

            if not existing_user:

                existing_user = User(
                    google_id=google_user["sub"],
                    email=google_user["email"],
                    full_name=google_user["name"],
                    profile_picture=google_user.get("picture")
                )

                db.add(existing_user)
                db.commit()
                db.refresh(existing_user)

            request.session["user"] = {
                "name": google_user.get("name"),
                "email": google_user.get("email"),
                "picture": google_user.get("picture")
            }

            request.session["user_id"] = existing_user.id

            return RedirectResponse(
                url="/dashboard",
                status_code=303
            )

        finally:
            db.close()

    except Exception as e:

        print("=" * 50)
        print("GOOGLE CALLBACK ERROR")
        print(type(e))
        print(e)
        print("=" * 50)

        raise

   

