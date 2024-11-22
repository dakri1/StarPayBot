from sqlalchemy.orm import Session

from database.connection import engine
from database.models import Subscription

async def get_subscription(tg_id):
    with Session(autoflush=False, bind=engine) as session:
        sub = session.query(Subscription).filter(Subscription.tg_id == tg_id).one_or_none()
        print(sub)
        return sub
