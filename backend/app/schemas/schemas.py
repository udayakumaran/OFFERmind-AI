from pydantic import BaseModel
from typing import Optional, List, Any, Dict

class CustomerBase(BaseModel):
    name: str
    email: str
    age: int
    location: str
    data_gb: float
    call_mins: int
    sms_count: int

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: int

    class Config:
        from_attributes = True

class SegmentBase(BaseModel):
    name: str
    description: str
    rules_json: Dict[str, Any]

class SegmentCreate(SegmentBase):
    pass
    
class SegmentResponse(SegmentBase):
    id: int

    class Config:
        from_attributes = True

class OfferBase(BaseModel):
    title: str
    description: str
    eligibility_criteria: Dict[str, Any]
    channel: str

class OfferCreate(OfferBase):
    pass

class OfferResponse(OfferBase):
    id: int

    class Config:
        from_attributes = True

class CustomerOfferResponse(BaseModel):
    id: int
    customer_id: int
    offer_id: int
    status: str
    message: Optional[str] = None
    
    class Config:
        from_attributes = True

class RecommendationRequest(BaseModel):
    customer_id: int
