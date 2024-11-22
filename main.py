import asyncio
import datetime
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from dotenv import load_dotenv

from database.create_subscription import create_subscription
from database.get_all_subs import get_all_subs
from database.get_subscription import get_subscription
from database.subscription_end import subscription_end
from database.subscription_paid import subscription_paid

load_dotenv()

TOKEN = os.getenv('TOKEN')
GROUP_ID = os.getenv('GROUP_ID')

bot = Bot(TOKEN)

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start(message: Message):
    if await get_subscription(message.chat.id) is None:
        await create_subscription(message.chat.id)

    await message.answer_invoice(title='Доступ в приват',
                                 description='Доступ в приват',
                                 payload='private',
                                 currency='XTR',
                                 prices=[LabeledPrice(label='XTR', amount=99)],
                                 )


@dp.pre_checkout_query()
async def pre_checkout_query(query: PreCheckoutQuery):
    await query.answer(True)

@dp.message(F.successful_payment)
async def successful_payment(message: Message):
    await subscription_paid(message.chat.id)
    await message.bot.refund_star_payment(message.from_user.id,
                                          message.successful_payment.telegram_payment_charge_id)
    link = await message.bot.create_chat_invite_link(chat_id=GROUP_ID, member_limit=1)

    await message.answer(link.invite_link)


async def send_periodic_messages():
    while True:
        await asyncio.sleep(86400)  # Задержка 24 часа (86400 секунд)

        # Получаем всех подписчиков
        subs = await get_all_subs()
        current_date = datetime.datetime.now()

        for sub in subs:
            try:
                # Уведомляем за 2 дня до завершения подписки
                if sub.paid and (sub.subscription_end_date - current_date).days == 2:
                    await bot.send_invoice(
                        chat_id=sub.tg_id,
                        title='Доступ в приват',
                        description='Ваша подписка скоро закончится через 2 дня. Пожалуйста, продлите её.',
                        payload='private',
                        currency='XTR',
                        prices=[LabeledPrice(label='XTR', amount=99)],
                    )

                # Если подписка закончилась
                if sub.paid and sub.subscription_end_date < current_date:
                    await subscription_end(sub.tg_id)
                    await bot.unban_chat_member(GROUP_ID, sub.tg_id)
                    await bot.send_invoice(
                        chat_id=sub.tg_id,
                        title='Доступ в приват',
                        description='Ваша подписка истекла, чтобы продолжить пользоваться, нужно продлить подписку',
                        payload='private',
                        currency='XTR',
                        prices=[LabeledPrice(label='XTR', amount=99)],
                    )

            except Exception as e:
                print(f"Ошибка при отправке сообщения: {e}")

async def main():
    asyncio.create_task(send_periodic_messages())
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())