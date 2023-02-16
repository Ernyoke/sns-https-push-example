import requests
import json
import xml.etree.ElementTree as ET
import boto3
from datetime import datetime

dynamodb = boto3.client('dynamodb')


def lambda_handler(event, context):
    message_type = event.get('headers', {}).get('x-amz-sns-message-type')
    subscriptionArn = event.get('headers', {}).get(
        'x-amz-sns-subscription-arn')
    body = json.loads(event.get('body', "{}"))

    if message_type == 'SubscriptionConfirmation':
        handle_subscribe(body)
    elif message_type == 'Notification':
        handle_notification(body, subscriptionArn)
    elif message_type == 'UnsubscribeConfirmation':
        handle_unsubscribe(body, subscriptionArn)
    else:
        raise Exception(f'Invalid message type: {message_type}!')

    return {
        "statusCode": 200
    }


def handle_subscribe(message):
    print("SUB_MESSAGE:", message)
    response = requests.get(message['SubscribeURL'])
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        arn, * \
            _ = root.findall(
                ".//{*}ConfirmSubscriptionResult/{*}SubscriptionArn")
        dynamodb.put_item(TableName='SNSSubs',
                          Item={'SubscriptionARN': {'S': arn.text},
                                'TopicArn': {'S': message['TopicArn']},
                                'SubStatus': {'S': 'Subscribed'},
                                'SubscribedTimeStamp': {'S': datetime.now().isoformat(timespec='seconds')}
                                })
    else:
        raise Exception(
            f'Could not accept subscription, response status code: {response.status_code}, response body: {response.text}')


def handle_notification(message, subscriptionArn):
    print("BODY:", message)
    print("SUB_ARN:", subscriptionArn)


def handle_unsubscribe(message, subscriptionArn):
    print("UNSUB:", message)
    dynamodb.update_item(TableName='SNSSubs', Key={
                         'SubscriptionARN': {'S': subscriptionArn}},
                         UpdateExpression='SET UnsubscibedTimestamp = :timestamp, SubStatus = :substatus',
                         ConditionExpression='attribute_exists(SubscriptionARN)',
                         ExpressionAttributeValues={
                             ':timestamp': {'S': datetime.now().isoformat(timespec='seconds')},
                             ':substatus': {'S': 'Unsubscribed'}},
                         )


if __name__ == "__main__":
    lambda_handler({'headers': {
        'x-amz-sns-message-type': 'SubscriptionConfirmation'
    }}, {})
