
from drugs_shooting_list.communication import process_message


def message_handler(event, context):
    print('Handle request ' + str(event), flush=True)
    try:
        process_message(event)
    except Exception as e:
        print('Handler error: ', e, flush=True)

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'isBase64Encoded': False,
        'body': 'success'
    }
