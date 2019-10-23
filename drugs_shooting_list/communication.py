from drugs_shooting_list.bot import bot, notify_admin
from drugs_shooting_list.settings import ADMIN_UID
from drugs_shooting_list.utils import to_tg_update, get_drug_info


greeting_msg = 'Добро пожаловать'


@to_tg_update(bot)
def process_message(update):

    text = update.message.text
    user_chat_id = update.message.chat.id

    if text == '/start':
        bot.send_message(
            user_chat_id,
            greeting_msg,
        )
        result = f'New user {user_chat_id}'
    else:

        result = get_drug_info(text)

        bot.send_message(
            user_chat_id,
            result
        )

    if user_chat_id != ADMIN_UID:
        user = update.message.from_user

        notify_admin(
            f'{user_chat_id} @{user.name} {user.username} {user.first_name} {user.last_name} {user.username}: {text}\n{result}')
