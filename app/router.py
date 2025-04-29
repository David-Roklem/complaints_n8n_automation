from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import schemas
import services.crud as crud
from services import text_analyzer
from database import db_helper
from services.crud import complaint_create, complaint_update

router = APIRouter(tags=["Main"])


@router.post("/complaints/", response_model=schemas.ComplaintResponse)
async def create_complaint(
    complaint_text: schemas.ComplaintCreate,
    session: AsyncSession = Depends(db_helper.get_session_dependency),
):
    text = complaint_text.text
    sentiment, category, is_spam = await text_analyzer.get_text_features(text)

    if all([sentiment, category]):
        complaint_data = {
            "text": text,
            "sentiment": sentiment,
            "status": "open",
            "category": category,
            "is_spam": is_spam,
        }
        return await complaint_create(session, complaint_data)
    return {"text": "Error occured... Damn it!"}


@router.get("/complaints/")
async def get_open_complaints_last_hour(
    session: AsyncSession = Depends(db_helper.get_session_dependency),
):
    return await crud.complaints_get(session)


@router.patch("/complaints/", response_model=schemas.ComplaintResponse)
async def update_complaint_status(
    update_data: schemas.ComplaintUpdate,
    session: AsyncSession = Depends(db_helper.get_session_dependency),
):
    return await complaint_update(session, update_data)
