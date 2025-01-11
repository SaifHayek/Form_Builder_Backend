from fastapi import FastAPI
from database import create_db_and_tables
from routes.form_routes import router as form_router
from fastapi.middleware.cors import CORSMiddleware






app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    
# /api/v1  

app.include_router(form_router, prefix='/forms', tags=['Forms'])

    
@app.get('/')
async def root():
     return {"message": "Welcome to the Form Builder API"}
        
    