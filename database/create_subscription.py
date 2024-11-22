from sqlalchemy.orm import Session

from database.connection import engine
from database.models import Subscription

async def create_subscription(tg_id):
    with Session(autoflush=True, bind=engine) as session:
        sub = Subscription(paid=False, tg_id=tg_id)
        print(sub)
        session.add(sub)
        session.commit()
