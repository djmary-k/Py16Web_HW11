from datetime import date, timedelta

from fastapi import HTTPException
from sqlalchemy import select, between
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, and_, extract, cast, Date

from src.entity.models import Contact
from src.schemas.contact import ContactBase, ContactUpdate


async def get_contacts(limit: int, offset: int, first_name: str, last_name: str, email: str, db: AsyncSession):
    statement = select(Contact).offset(offset).limit(limit)

    conditions = []
    if first_name:
        conditions.append(Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        conditions.append(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        conditions.append(Contact.email.ilike(f"%{email}%"))

    if conditions:
        statement = statement.filter(and_(*conditions))

    contacts = await db.execute(statement)
    await db.close()
    return contacts.scalars().all()


async def get_contacts_by_id(contact_id: int, db: AsyncSession):
    statement = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(statement)
    await db.close()
    return contact.scalar_one_or_none()


async def create_contact(body: ContactBase, db: AsyncSession):
    try:
        contact = Contact(**body.model_dump())
        db.add(contact)
        await db.commit()
        await db.refresh(contact)
        return contact
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await db.close()


async def update_contact(contact_id: int, contact: ContactUpdate, db: AsyncSession):
    statement = select(Contact).filter_by(id=contact_id)
    existing_contact = await db.execute(statement)
    existing_contact = existing_contact.scalar_one_or_none()
    if existing_contact:
        for key, value in contact.model_dump().items():
            setattr(existing_contact, key, value)
        await db.commit()
        await db.refresh(existing_contact)
        await db.close()
    return existing_contact


async def delete_contact(contact_id: int, db: AsyncSession):
    statement = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(statement)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
        return contact


async def get_upcoming_birthdays(db: AsyncSession):
    today = date.today()
    next_week = today + timedelta(days=7)

    statement = select(Contact).filter(
        between(
            cast(Contact.birthday, Date),
            cast(today, Date),
            cast(next_week, Date)
        )
    )

    contacts = await db.execute(statement)
    await db.close()
    return contacts.scalars().all()