from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from models.recommendation import Recommendation
from services.gemini_service import generate_home_recommendations

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/home")
def home_page(request: Request):
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={}
    )


@router.post("/generate-home")
def generate_home(
    request: Request,
    budget: int = Form(...),
    room_type: str = Form(...),
    items: list[str] = Form([]),
    db: Session = Depends(get_db)
):
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    recommendations = generate_home_recommendations(
        budget,
        room_type,
        items
    )

    if not recommendations.startswith("Gemini error:"):
        new_recommendation = Recommendation(
            user_id=user_id,
            category="Home",
            input_details=(
                f"Budget: ₹{budget}, "
                f"Room: {room_type}, "
                f"Items: {', '.join(items) if items else 'General'}"
            ),
            recommendation=recommendations
        )

        db.add(new_recommendation)
        db.commit()

    return templates.TemplateResponse(
        request=request,
        name="home_result.html",
        context={
            "budget": budget,
            "room_type": room_type,
            "items": items,
            "recommendations": recommendations
        }
    )