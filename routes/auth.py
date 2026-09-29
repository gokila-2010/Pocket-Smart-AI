from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Form, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from jose import jwt
import bcrypt

from database import get_db
from models.user import User
from models.recommendation import Recommendation

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# JWT settings
SECRET_KEY = "pocketsmart-jwt-secret-key-change-later"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={"request": request}
    )


@router.post("/register")
def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == email
    ).first()

    if existing_user:
        return HTMLResponse(
            """
            <h3>Email already registered.</h3>
            <a href="/register">Try again</a>
            """
        )

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    new_user = User(
        username=username,
        email=email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()

    return RedirectResponse(
        url="/login",
        status_code=303
    )


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"request": request}
    )


@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        return HTMLResponse(
            """
            <h3>Invalid email or password.</h3>
            <a href="/login">Try again</a>
            """
        )

    stored_password = user.password

    if stored_password.startswith("$2"):
        password_valid = bcrypt.checkpw(
            password.encode("utf-8"),
            stored_password.encode("utf-8")
        )
    else:
        password_valid = (password == stored_password)

        if password_valid:
            user.password = bcrypt.hashpw(
                password.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")
            db.commit()

    if not password_valid:
        return HTMLResponse(
            """
            <h3>Invalid email or password.</h3>
            <a href="/login">Try again</a>
            """
        )

    request.session["user_id"] = user.id
    request.session["username"] = user.username

    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )


# ---------------------------------------------------------
# JWT TOKEN ROUTE
# ---------------------------------------------------------

@router.post("/token")
def create_token(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        return HTMLResponse(
            """
            <h3>Invalid email or password.</h3>
            """
        )

    stored_password = user.password

    if stored_password.startswith("$2"):
        password_valid = bcrypt.checkpw(
            password.encode("utf-8"),
            stored_password.encode("utf-8")
        )
    else:
        password_valid = (password == stored_password)

    if not password_valid:
        return HTMLResponse(
            """
            <h3>Invalid email or password.</h3>
            """
        )

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    token_data = {
        "sub": str(user.id),
        "username": user.username,
        "email": user.email,
        "exp": expire
    }

    access_token = jwt.encode(
        token_data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
@router.get("/session-info")
def session_info(request: Request):
    user_id = request.session.get("user_id")
    username = request.session.get("username")

    if not user_id:
        return {
            "logged_in": False,
            "user_id": None,
            "username": None
        }

    return {
        "logged_in": True,
        "user_id": user_id,
        "username": username
    }
@router.get("/session-data")
def session_data(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    username = request.session.get("username")

    if not user_id:
        return {
            "logged_in": False,
            "user_id": None,
            "username": None,
            "recommendations": []
        }

    recommendations = (
        db.query(Recommendation)
        .filter(Recommendation.user_id == user_id)
        .order_by(Recommendation.id.desc())
        .all()
    )

    return {
        "logged_in": True,
        "user_id": user_id,
        "username": username,
        "recommendations": [
            {
                "id": item.id,
                "category": item.category,
                "input_details": item.input_details,
                "recommendation": item.recommendation
            }
            for item in recommendations
        ]
    }
@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    username = request.session.get("username")

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "username": username
        }
    )


@router.get("/logout")
def logout(request: Request):
    request.session.clear()

    return RedirectResponse(
        url="/login",
        status_code=303
    )