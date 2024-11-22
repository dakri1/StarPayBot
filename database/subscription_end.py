import datetime

from sqlalchemy.orm import Session

from database.connection import engine
from database.create_subscription import create_subscription
from database.get_subscription import get_subscription
from database.models import Subscription


async def subscription_end(tg_id):
    with Session(autoflush=False, bind=engine) as session:
        sub = session.query(Subscription).filter(Subscription.tg_id == tg_id).one_or_none()
        if sub is None:
           sub = Subscription(paid=False, tg_id=tg_id)
           session.add(sub)
           session.commit()
        sub.paid = False
        session.commit()
