from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models import models
from ..schemas import schemas
from ..agents.orchestrator import run_orchestrator

router = APIRouter()

@router.get("/customers", response_model=List[schemas.CustomerResponse])
def get_customers(db: Session = Depends(get_db)):
    return db.query(models.Customer).all()

@router.post("/customers", response_model=schemas.CustomerResponse)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.get("/offers", response_model=List[schemas.OfferResponse])
def get_offers(db: Session = Depends(get_db)):
    return db.query(models.Offer).all()

@router.post("/offers", response_model=schemas.OfferResponse)
def create_offer(offer: schemas.OfferCreate, db: Session = Depends(get_db)):
    db_offer = models.Offer(**offer.model_dump())
    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)
    return db_offer

@router.post("/recommend", response_model=schemas.CustomerOfferResponse)
def generate_recommendation(req: schemas.RecommendationRequest, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == req.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Run the agent workflow
    result = run_orchestrator(schemas.CustomerResponse.model_validate(customer).model_dump(), db)
    
    # Save the recommendation
    offer = db.query(models.Offer).filter(models.Offer.title == result["offer_title"]).first()
    
    customer_offer = models.CustomerOffer(
        customer_id=customer.id,
        offer_id=offer.id if offer else None,
        status="generated",
        message=result["personalized_message"]
    )
    db.add(customer_offer)
    db.commit()
    db.refresh(customer_offer)
    
    return customer_offer

@router.get("/customer-offers", response_model=List[schemas.CustomerOfferResponse])
def get_customer_offers(db: Session = Depends(get_db)):
    return db.query(models.CustomerOffer).all()
