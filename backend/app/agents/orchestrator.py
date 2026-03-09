from sqlalchemy.orm import Session
from ..models import models

def run_orchestrator(customer: dict, db: Session):
    """
    Mock LangGraph Multi-Agent Orchestrator
    In a real-world scenario, you would put the LangGraph StateGraph logic here
    and orchestrate the 4 Agents (SegmentAgent, ProfileAnalyzer, OfferAgent, PersonalizeAgent).
    """
    
    # 1. Profile Analyzer (Mock)
    profile_summary = f"{customer['name']} is {customer['age']} years old from {customer['location']}."
    if customer['data_gb'] > 50:
        profile_summary += " High data usage."
    
    # 2. Segment Agent (Mock Rule-based extraction)
    segment = "Standard User"
    if customer['data_gb'] > 100:
        segment = "Heavy Data User"
    elif customer['call_mins'] > 1000:
        segment = "Talkative User"
        
    # 3. Offer Matching Agent (Mock)
    # Get available offers
    all_offers = db.query(models.Offer).all()
    offer_title = "Standard Bundle"
    channel = "Email"
    if segment == "Heavy Data User" and any(o.title == "Unlimited Data Plus" for o in all_offers):
        offer_title = "Unlimited Data Plus"
        channel = "SMS"
    elif segment == "Talkative User" and any(o.title == "Global Calling Plan" for o in all_offers):
        offer_title = "Global Calling Plan"
        
    # 4. Personalize Message Agent (Mock LLM)
    custom_msg = f"Hi {customer['name']}, we noticed your impressive data usage! Upgrade to our {offer_title} to stay connected endlessly."
    if segment == "Talkative User":
        custom_msg = f"Hey {customer['name']}! Enjoy endless calls with our {offer_title} tailored just for {customer['location']} residents."
    
    return {
        "segment": segment,
        "profile_summary": profile_summary,
        "offer_title": offer_title,
        "channel": channel,
        "personalized_message": custom_msg
    }
