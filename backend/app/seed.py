import random
from sqlalchemy.orm import Session
from .core.database import SessionLocal, engine, Base
from .models import models

def seed_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Clear existing data
    db.query(models.CustomerOffer).delete()
    db.query(models.Customer).delete()
    db.query(models.Segment).delete()
    db.query(models.Offer).delete()
    db.commit()

    print("Seeding segments...")
    segments = [
        models.Segment(name="Standard User", description="Average usage", rules_json={"data_gb_min": 0, "data_gb_max": 50}),
        models.Segment(name="Heavy Data User", description="Uses more than 100GB", rules_json={"data_gb_min": 100}),
        models.Segment(name="Talkative User", description="Makes lots of calls", rules_json={"call_mins_min": 1000}),
    ]
    db.add_all(segments)

    print("Seeding offers...")
    offers = [
        models.Offer(title="Standard Bundle", description="10GB Data & 500 mins", eligibility_criteria={"segment": "Standard User"}, channel="SMS"),
        models.Offer(title="Unlimited Data Plus", description="Unlimited 5G Data", eligibility_criteria={"segment": "Heavy Data User"}, channel="Email"),
        models.Offer(title="Global Calling Plan", description="Unlimited International Calls", eligibility_criteria={"segment": "Talkative User"}, channel="App Push"),
    ]
    db.add_all(offers)

    print("Seeding 100 customers...")
    locations = ["New York", "London", "Tokyo", "Berlin", "Sydney", "Mumbai", "Toronto", "Paris"]
    first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
    
    customers = []
    for i in range(100):
        c = models.Customer(
            name=f"{random.choice(first_names)} {random.choice(last_names)}",
            email=f"user{i}@example.com",
            age=random.randint(18, 75),
            location=random.choice(locations),
            data_gb=round(random.uniform(5.0, 250.0), 2),
            call_mins=random.randint(50, 2000),
            sms_count=random.randint(0, 500)
        )
        customers.append(c)
    
    db.add_all(customers)
    db.commit()
    print("Seeding complete.")
    db.close()

if __name__ == "__main__":
    seed_data()
