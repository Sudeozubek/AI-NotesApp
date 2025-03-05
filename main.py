from fastapi import FastAPI
from models.models import Base
from database.database import engine
from fastapi.middleware.cors import CORSMiddleware
from routers.note import router as notes_router
 
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],   
)
Base.metadata.create_all(bind=engine)

app.include_router(notes_router)

@app.get("/")
async def home():
    return {"message": "AI-Powered Notes App is running"}
