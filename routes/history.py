from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from models.recommendation import Recommendation

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/history")
def history_page(
    request: Request,
    db: Session = Depends(get_db)
):
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    recommendations = (
        db.query(Recommendation)
        .filter(Recommendation.user_id == user_id)
        .order_by(Recommendation.id.desc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "recommendations": recommendations
        }
    )
@router.get("/recommendations-details")
def recommendations_details(
    request: Request,
    db: Session = Depends(get_db)
):
    user_id = request.session.get("user_id")

    if not user_id:
        return {
            "logged_in": False,
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