from sqlmodel import Field, SQLModel, Column
from sqlalchemy.dialects.postgresql import JSONB
from pydantic import BaseModel, model_validator
from typing import List
from enum import Enum

class FieldType(Enum):
    TEXT = "text"
    EMAIL = "email"
    SELECT = "select"
    TEXTAREA = "textarea"
    RADIO = "radio"
    NUMBER = "number"
    PASSWORD = "password"
    CHECKBOX = "checkbox"


class ValidationModel(BaseModel):
    required: bool
    hide: bool
    min_length: int | None = Field(default=None, ge=0)
    max_length: int | None = Field(default=None, ge=0)
    min_value: int | None = Field(default=None)
    max_value: int | None = Field(default=None)
    

    

class ChoicesModel(BaseModel):
    id: str
    label: str = Field(nullable=False, min_length=1, max_length=255)
    value: str = Field(nullable=False, min_length=1, max_length=255)
    

class FormFieldModel(BaseModel):
    id: str
    type: FieldType
    placeholder_en: str | None = Field(default="")
    placeholder_ar: str | None = Field(default="")
    order: int = Field(gt=0)
    label_en: str = Field(nullable=False)
    label_ar: str = Field(nullable=False)
    choices: List[ChoicesModel] | None = Field(sa_column=Column(JSONB), default_factory=list)
    validation: ValidationModel = Field(sa_column=Column(JSONB))
    
        
class Form(SQLModel, table=True):
    __tablename__ = "forms"
    id: int = Field(primary_key=True)
    title_en: str = Field(index=True, nullable=False, unique=True)
    title_ar: str = Field(index=True, nullable=False, unique=True)
    fields: List[FormFieldModel] = Field(sa_column=Column(JSONB), default_factory=list)
    

    


    @model_validator(mode='after')
    def validate_fields_not_empty(self):
        if not self.fields:
            raise ValueError("Fields cannot be empty.")
        if not isinstance(self.fields, list):
            raise ValueError("Fields must be a list")            
        return self
    
    
    @model_validator(mode='after')
    def validate_fields(self):
        for field in self.fields:
            self.create_form_field_model_from_dict(field) 
            if field['type'] in ['select', 'radio']: 
                field['choices'] = self.create_choices_from_dict(field['choices'])
                
            if field['type'] in ['text', 'textarea', 'password']:
                self._validate_length(field)
                    
            if field['type'] in ['number']:
                self._validate_numeric_values(field)
                    
            if field['validation']['hide'] and field['validation']['required']:
                raise ValueError("Hide and required cannot be true at the same time")
                
            
        return self    
        
        
    def _validate_length(self, field):
            if 'min_length' in field['validation'] and 'max_length' in field['validation']:
                    if field['validation']['min_length'] > field['validation']['max_length']:
                        raise ValueError("Min length must be less than or equal max length")

    def _validate_numeric_values(self, field):
        if 'min_value' in field['validation'] and 'max_value' in field['validation']:
                    if field['validation']['min_value'] > field['validation']['max_value']:
                        raise ValueError("Min value must be less than max value")
            
    def create_choices_from_dict(self, data: List[dict]) -> List[ChoicesModel]:
        return [ChoicesModel(**choice_data) for choice_data in data]      
    
    def create_form_field_model_from_dict(self, data: dict) -> FormFieldModel:
        return FormFieldModel(**data)

    
    

    
    
    
    
    
    