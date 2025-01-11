from fastapi import  Query, HTTPException, APIRouter
from typing import Annotated
from models.form_model import Form
from database import SessionDep
from crud.form_curd import get_forms, get_form, create_form, delete_form, update_form

router = APIRouter()

@router.get('/')
async def list_forms(session: SessionDep, 
                     offset: int = 0 , 
                     limit: Annotated[int, Query(le=100)] = 100
                    ) -> list[Form]:
    return get_forms(session, offset, limit)


@router.get('/{id}')
async def retrieve_form(session: SessionDep, id: int):
    form = get_form(session, id)
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")
    return form

@router.post("/")
async def create_new_form(session: SessionDep, form: Form):
    return create_form(session, form)

@router.delete("/{id}")
async def delete_existing_form(session: SessionDep ,id: int):
    form = delete_form(session, id)
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")
    return {"message": "Form deleted successfully"}
    
    
@router.put("/{id}")
async def update_existing_form(session: SessionDep, id: int, updated_data: Form):
    form = update_form(session, id, updated_data)
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")
    return {"message": "Form updated successfully", "form": form}


