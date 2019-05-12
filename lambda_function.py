import shippostbot


def lambda_handler(event, context):
    shippostbot.create_post()
    return {
        'statusCode': 200
    }
