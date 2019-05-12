import shippostbot


def lambda_handler(event, context):
    try:
        res = shippostbot.main()
        return {
            'statusCode': 200,
            'data': res.json()
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'error': str(e)
        }
