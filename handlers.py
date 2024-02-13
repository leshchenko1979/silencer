import datetime as dt

from aiogram import Dispatcher, F, types
from aiogram.filters.chat_member_updated import MEMBER, ChatMemberUpdatedFilter
from aiogram.types import Chat, ChatMemberUpdated, User
from aiogram.enums import ChatType

from yandex_logging import logger

INITIAL_SILENCE_DAYS = 1
SELF_USERNAME = "flipper_club_moderator_bot"

dp = Dispatcher()


@dp.message(F.new_chat_members)
async def on_user_join(message: types.Message):
    for new_chat_member in message.new_chat_members:
        await restrict_user(message.chat, new_chat_member)


# не смотрим на обновления в каланах, только группы
dp.chat_member.filter(F.chat.type == ChatType.SUPERGROUP)


@dp.chat_member(ChatMemberUpdatedFilter(MEMBER))
async def on_user_return(chat_member: ChatMemberUpdated):
    await restrict_user(chat_member.chat, chat_member.from_user)


async def restrict_user(chat: Chat, user: User):
    if user.username == SELF_USERNAME:
        return

    logger.info(
        f"Restricting user {user.username or user.id} "
        f"in chat {chat.username or chat.id}"
    )

    assert await chat.restrict(
        user_id=user.id,
        permissions=types.chat_permissions.ChatPermissions(can_send_messages=False),
        until_date=dt.datetime.now(tz=dt.timezone.utc)
        + dt.timedelta(days=INITIAL_SILENCE_DAYS),
    )
