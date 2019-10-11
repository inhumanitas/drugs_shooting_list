
from drugs_shooting_list.bot import bot
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

    bot.send_message(
        update.message.chat.id,
        get_drug_info(update.message.text)
    )

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'isBase64Encoded': False,
        'body': 'success'
    }
