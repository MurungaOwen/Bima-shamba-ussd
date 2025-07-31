from db import SessionLocal, engine
from models import Base, Policy

Base.metadata.create_all(bind=engine)
db = SessionLocal()

default_policies = [
    {"name": "Maize Cover", "description": "Covers drought and pests", "premium_amount": "500"},
    {"name": "Beans Shield", "description": "Covers floods", "premium_amount": "300"},
    {"name": "Greenhouse Cover", "description": "Covers structure damage", "premium_amount": "800"},
]

for p in default_policies:
    policy = Policy(**p)
    db.add(policy)

db.commit()
db.close()
