from telegram import ParseMode

from drugs_shooting_list.bot import bot, notify_admin
from drugs_shooting_list.utils import get_drug_info, to_tg_update


def echo_handler(update, context):

    bot.send_message(
        update.message.chat.id,
        update.message.text
    )

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'isBase64Encoded': False,
        'body': 'success'
    }


@to_tg_update(bot)
def message_handler(update, context):
    result = get_drug_info(update.message.text)
    bot.send_message(
        update.message.chat.id,
        result,
        disable_web_page_preview=True,
        parse_mode=ParseMode.HTML,
    )
    user = update.message.from_user
    notify_admin(f'{update.message.chat.id} @{user.name} {user.username} {user.first_name} {user.last_name} {user.username}: {update.message.text}\n{result}')

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'isBase64Encoded': False,
        'body': 'success'
    }
