from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text

from src.settings.config import engine, get_db
from src.database import models
from src.routers.contacts import router as contacts_router

app = FastAPI(title="Contacts API")

models.Base.metadata.create_all(bind=engine)

@app.get("/api/healthchecker")
def get_health_status(db=Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1+1")).fetchone()
        if result is None:
            raise Exception
        return {"message": "Welcome to FastAPI", "status": "OK"}
    except Exception:
        raise HTTPException(status_code=503, detail="Database is not available")

app.include_router(contacts_router, prefix="/api")
