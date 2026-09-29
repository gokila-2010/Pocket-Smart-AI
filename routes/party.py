from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from models.recommendation import Recommendation
from services.gemini_service import generate_party_recommendations

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/party")
def party_page(request: Request):
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="party.html",
        context={}
    )


@router.post("/generate-party")
def generate_party(
    request: Request,
    budget: int = Form(...),
    guest_count: int = Form(...),
    event_type: str = Form(...),
    venue: str = Form(...),
    db: Session = Depends(get_db)
):
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    recommendations = generate_party_recommendations(
        budget=budget,
        guest_count=guest_count,
        event_type=event_type,
        venue=venue
    )

    if not recommendations.startswith("Gemini error:"):
        new_recommendation = Recommendation(
            user_id=user_id,
            category="Party",
            input_details=(
                f"Budget: ₹{budget}, "
                f"Guests: {guest_count}, "
                f"Event: {event_type}, "
                f"Venue: {venue}"
            ),
            recommendation=recommendations
        )

        db.add(new_recommendation)
        db.commit()

    return templates.TemplateResponse(
        request=request,
        name="party_result.html",
        context={
            "budget": budget,
            "guest_count": guest_count,
            "event_type": event_type,
            "venue": venue,
            "recommendations": recommendations
        }
    )