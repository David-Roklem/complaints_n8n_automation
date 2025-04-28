from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Complaint
from schemas import ComplaintUpdate, StatusEnum


async def complaint_create(session: AsyncSession, complaint_data: dict) -> Complaint:
    try:
        complaint = Complaint(**complaint_data)
        session.add(complaint)
        await session.commit()
    except Exception:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error"
        )
    return complaint


async def complaint_update(session: AsyncSession, update_data: ComplaintUpdate) -> Complaint:
    try:
        # Находим существующую жалобу по ID
        stmt = select(Complaint).where(Complaint.id == update_data.id)
        result = await session.execute(stmt)
        complaint = result.scalar_one_or_none()

        if complaint is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Complaint not found"
            )

        # Обновляем поле статуса
        complaint.status = "closed"

        await session.commit()
        return complaint

    except Exception:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error"
        )


async def complaints_get(session: AsyncSession):
    # Определяем временной интервал (последний час).
    # Также отнимаю разницу между московским временем и UTC
    # Данный костыль обходит проблему работы в SQLite с timezone
    one_hour_ago = datetime.now() - timedelta(hours=4)
    stmt = select(Complaint).filter(
        and_(
            Complaint.status == StatusEnum.OPEN.value,
            Complaint.timestamp >= one_hour_ago,
            datetime.now() >= Complaint.timestamp,
        )
    )

    result = await session.scalars(stmt)
    return result.all()
