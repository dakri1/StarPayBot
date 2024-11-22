import datetime

from sqlalchemy.orm import Session

from database.connection import engine
from database.create_subscription import create_subscription
from database.get_subscription import get_subscription
from database.models import Subscription


async def subscription_paid(tg_id):
    with Session(autoflush=False, bind=engine) as session:
        sub = session.query(Subscription).filter(Subscription.tg_id == tg_id).one_or_none()
        if sub is None:
           print("sub is none")
           sub = Subscription(paid=False, tg_id=tg_id)
           session.add(sub)
           session.commit()

        if sub.paid:
            sub.subscription_end_date = sub.subscription_end_date + datetime.timedelta(minutes=5)
        else:
            sub.subscription_end_date = datetime.datetime.now() + datetime.timedelta(minutes=5)
        print(sub.tg_id)
        sub.paid = True
        print(sub.subscription_end_date)
        session.commit()
