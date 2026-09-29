from fastapi import APIRouter, Request, Form, UploadFile, File, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from models.recommendation import Recommendation
from services.gemini_service import generate_jewelry_recommendations

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/jewelry")
def jewelry_page(request: Request):
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="jewelry.html",
        context={}
    )


@router.post("/generate-jewelry")
async def generate_jewelry(
    request: Request,
    budget: int = Form(...),
    occasion: str = Form(...),
    style: str = Form(...),
    outfit_image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    image_bytes = None
    image_mime_type = None

    if outfit_image and outfit_image.filename:
        image_bytes = await outfit_image.read()
        image_mime_type = outfit_image.content_type

    recommendations = generate_jewelry_recommendations(
        budget=budget,
        occasion=occasion,
        style=style,
        image_bytes=image_bytes,
        image_mime_type=image_mime_type
    )

    if not recommendations.startswith("Gemini error:"):
        if not recommendations.startswith(
            "Image analysis is currently unavailable"
        ):
            new_recommendation = Recommendation(
                user_id=user_id,
                category="Jewelry",
                input_details=(
                    f"Budget: ₹{budget}, "
                    f"Occasion: {occasion}, "
                    f"Style: {style}"
                ),
                recommendation=recommendations
            )

            db.add(new_recommendation)
            db.commit()

    return templates.TemplateResponse(
        request=request,
        name="jewelry_result.html",
        context={
            "budget": budget,
            "occasion": occasion,
            "style": style,
            "recommendations": recommendations
        }
    )