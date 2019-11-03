from uuid import uuid4

from telegram import ParseMode, InlineQueryResultArticle, \
    InputTextMessageContent

from drugs_shooting_list.bot import bot, notify_admin
from drugs_shooting_list.settings import ADMIN_UID
from drugs_shooting_list.utils import to_tg_update, get_drug_info, predict_key, \
    DATA

greeting_msg = 'Добро пожаловать'


def inline_search(update):
    """Handle the inline query."""
    query = update.inline_query.query
    results = [
        InlineQueryResultArticle(
            id=uuid4(), title=x,
            input_message_content=InputTextMessageContent(
                get_drug_info(x), parse_mode=ParseMode.HTML))
        for x in DATA.get_subkeys(query.lower())
    ]
    return update.inline_query.answer(results)


@to_tg_update(bot)
def process_message(update):
    if update.inline_query:
        print('inline_search ' + str(update.inline_query))
        return inline_search(update)

    if not update.message:
        return

    text = update.message.text
    user_chat_id = update.message.chat.id

    if text == '/start':
        print('Greeting new user ' + str(user_chat_id))
        bot.send_message(
            user_chat_id,
            greeting_msg,
        )
        result = f'New user {user_chat_id}'

    else:
        result = get_drug_info(text)
        if result:
            bot.send_message(
                user_chat_id,
                result,
                disable_web_page_preview=True,
                parse_mode=ParseMode.HTML,
            )
        else:
            keys = predict_key(text, words=5)
            result = 'Не найдено. Попробуйте варианты: ' + ', '.join(keys)
            bot.send_message(
                user_chat_id,
                result,
                disable_web_page_preview=True,
                parse_mode=ParseMode.HTML,
            )

    if user_chat_id != ADMIN_UID:
        user = update.message.from_user

        notify_admin(
            f'{user_chat_id} @{user.name} {user.username} {user.first_name} {user.last_name} {user.username}: {text}\n{result}')
