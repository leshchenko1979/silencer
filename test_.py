from unittest.mock import Mock

import aiogram
import pytest
from aiogram.types.update import Update

import handlers
from handlers import dp


@pytest.mark.parametrize(
    "raw_update",
    [
        '{"update_id":13671261,"message":{"message_id":118,"from":{"id":133526395,"is_bot":false,"first_name":"\u0410\u043b\u0435\u043a\u0441\u0435\u0439","last_name":"\u041b\u0435\u0449\u0435\u043d\u043a\u043e | \u0418\u043d\u0432\u0435\u0441\u0442-\u043d\u0435\u0434\u0432\u0438\u0436\u0438\u043c\u043e\u0441\u0442\u044c","username":"leshchenko1979","language_code":"ru","is_premium":true},"chat":{"id":-4165056164,"title":"test","type":"group","all_members_are_administrators":true},"date":1707572699,"text":"ask"}}',
    ],
)
def test_raw_update_validation(raw_update: str):
    Update.model_validate_json(raw_update)


def mocked_bot():
    return aiogram.Bot(token="123:test_token")


@pytest.mark.parametrize(
    "raw_update, decision",
    [
        (
            '{"update_id":13671281,"message":{"message_id":10,"from":{"id":133526395,"is_bot":false,"first_name":"\u0410\u043b\u0435\u043a\u0441\u0435\u0439","last_name":"\u041b\u0435\u0449\u0435\u043d\u043a\u043e | \u0418\u043d\u0432\u0435\u0441\u0442-\u043d\u0435\u0434\u0432\u0438\u0436\u0438\u043c\u043e\u0441\u0442\u044c","username":"leshchenko1979","language_code":"ru","is_premium":true},"chat":{"id":-1001765843568,"title":"test","username":"blabllablabla4","type":"supergroup"},"date":1707580640,"new_chat_participant":{"id":687341524,"is_bot":false,"first_name":"\u041f\u0435\u0442\u0440","last_name":"\u041b\u0435\u0449\u0435\u043d\u043a\u043e","username":"dafkinninja"},"new_chat_member":{"id":687341524,"is_bot":false,"first_name":"\u041f\u0435\u0442\u0440","last_name":"\u041b\u0435\u0449\u0435\u043d\u043a\u043e","username":"dafkinninja"},"new_chat_members":[{"id":687341524,"is_bot":false,"first_name":"\u041f\u0435\u0442\u0440","last_name":"\u041b\u0435\u0449\u0435\u043d\u043a\u043e","username":"dafkinninja"}]}}',
            "restrict",
        ),
        (
            '{"update_id":13671559,"chat_member":{"chat":{"id":-1001743416957,"title":"\u041a\u043b\u0443\u0431 \u0424\u043b\u0438\u043f\u043f\u0435\u0440\u043e\u0432 \u2014 \u043f\u043e\u043f\u0443\u043b\u044f\u0440\u043d\u043e\u0435","username":"flipping_club_digest","type":"channel"},"from":{"id":1868349823,"is_bot":false,"first_name":"Irina","last_name":"Sheremeteva","username":"Irina_Sheremeteva555"},"date":1707752362,"old_chat_member":{"user":{"id":1868349823,"is_bot":false,"first_name":"Irina","last_name":"Sheremeteva","username":"Irina_Sheremeteva555"},"status":"left"},"new_chat_member":{"user":{"id":1868349823,"is_bot":false,"first_name":"Irina","last_name":"Sheremeteva","username":"Irina_Sheremeteva555"},"status":"member"}}}',
            "pass",
        ),
    ],
    ids=["user_join", "update_on_channel_join"],
)
@pytest.mark.asyncio
async def test_restrict_user(raw_update: str, decision, monkeypatch):
    restrict_user_mock = Mock(spec=handlers.restrict_user)
    monkeypatch.setattr(handlers, "restrict_user", restrict_user_mock)

    await dp.feed_update(mocked_bot(), Update.model_validate_json(raw_update))

    if decision == "restrict":
        restrict_user_mock.assert_called_once()
    else:
        restrict_user_mock.assert_not_called()
