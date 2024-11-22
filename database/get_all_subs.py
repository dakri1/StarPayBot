from sqlalchemy.orm import Session

from database.connection import engine
from database.models import Subscription

async def get_all_subs():
    with Session(autoflush=False, bind=engine) as session:
        subs = session.query(Subscription).all()
        return subs
