
from drugs_shooting_list.communication import process_message


def message_handler(event, context):

    process_message(event)

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'isBase64Encoded': False,
        'body': 'success'
    }
