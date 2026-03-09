from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.database import engine, Base, SessionLocal
from .api import endpoints
from .models import models

# Create standard SQLite tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Telecom SaaS Multi-Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(endpoints.router, prefix="/api", tags=["api"])

@app.on_event("startup")
def auto_seed():
    """Auto-seed the database with sample data if it's empty."""
    db = SessionLocal()
    try:
        count = db.query(models.Customer).count()
        if count == 0:
            print("Database is empty — running auto-seed...")
            from .seed import seed_data
            seed_data()
            print("Auto-seed complete!")
        else:
            print(f"Database already has {count} customers — skipping seed.")
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Telecom SaaS API"}
