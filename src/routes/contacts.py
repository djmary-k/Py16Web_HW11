from typing import Optional, List

from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.repository import contacts as repository_contacts
from src.schemas.contact import ContactBase, ContactUpdate, ContactResponse

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get('/', response_model=List[ContactResponse])
async def get_contacts(
    limit: int = Query(10, ge=10, le=100),
    offset: int = Query(0, ge=0),
    first_name: Optional[str] = Query(None, title="Firstname filter"),
    last_name: Optional[str] = Query(None, title="Lastname filter"),
    email: Optional[str] = Query(None, title="Email filter"),
    db: AsyncSession = Depends(get_db)
):
    try:
        contacts = await repository_contacts.get_contacts(limit, offset, first_name, last_name, email, db)
        return contacts
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get('/{contacts_id}', response_model=ContactResponse)
async def get_contacts_by_id(contacts_id: int, db: AsyncSession = Depends(get_db)):
    try:
        contact = await repository_contacts.get_contact(contacts_id, db)
        if contact:
            return contact
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post('/', response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactBase, db: AsyncSession = Depends(get_db)):
    try:
        contact = await repository_contacts.create_contact(body, db)
        return contact
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put('/{contacts_id}', response_model=ContactResponse, status_code=status.HTTP_200_OK)
async def update_contact(contacts_id: int, body: ContactUpdate, db: AsyncSession = Depends(get_db)):
    try:
        contact = await repository_contacts.update_contact(contacts_id, body, db)
        if contact:
            return contact
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete('/{contacts_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contacts_id: int, db: AsyncSession = Depends(get_db)):
    try:
        contact = await repository_contacts.delete_contact(contacts_id, db)
        if contact:
            return contact
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/birthday/", response_model=List[ContactResponse])
async def get_upcoming_birthdays(db: AsyncSession = Depends(get_db)):
    try:
        contacts = await repository_contacts.get_upcoming_birthdays(db)
        return contacts
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
