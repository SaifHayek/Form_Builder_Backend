from fastapi import Query, HTTPException
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from typing import Annotated
from models.form_model import Form, FormFieldModel
from database import  SessionDep


def get_forms(session: SessionDep, 
               offset: int = 0 , 
               limit: Annotated[int, Query(le=100)] = 100):
    return session.exec(select(Form).offset(offset).limit(limit)).all()

def get_form(session: SessionDep, id: int):
    return session.get(Form, id)


def create_form(session: SessionDep, form: Form):
    try:
        form_data_dict = form.model_dump(exclude=['id'])
        form_data = Form(**form_data_dict) 
        session.add(form_data)
        session.commit()
        session.refresh(form_data)
        return form_data
    except IntegrityError as e:
        session.rollback()
        if "unique constraint" in str(e.orig).lower():
            raise HTTPException(status_code=400, detail="Form title must be unique.")
        raise HTTPException(status_code=500, detail="An error occurred while creating the form.")

def delete_form(session: SessionDep, id: int):
    form = session.get(Form, id)
    if form:
        session.delete(form)
        session.commit()
    return form


def update_form(session: SessionDep, id: int, updated_data: Form):
    form = session.get(Form, id)
    if form:
        form.title = updated_data.title
        form.fields = updated_data.fields
        session.commit()
        session.refresh(form)
    return form