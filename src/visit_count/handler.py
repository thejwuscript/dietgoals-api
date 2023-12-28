import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()


class Boto3Class(object):
    _instance = None

    def __new__(cls, service):
        if cls._instance is None:
            cls._instance = super(Boto3Class, cls).__new__(cls)
            cls._instance.resource = boto3.resource(service)
        return cls._instance


def get_visit_count(dynamodb_table) -> int:
    res = dynamodb_table.get_item(Key={"pk": "visitors", "sk": "visitors"})
    try:
        return res["Item"]["visit_count"]
    except Exception:
        raise ValueError("Cannot get item")


def increment_visit_count(dynamodb_table) -> int:
    res = dynamodb_table.update_item(
        Key={"pk": "visitors", "sk": "visitors"},
        ReturnValues="UPDATED_NEW",
        UpdateExpression="ADD visit_count :num",
        ExpressionAttributeValues={
            ":num": 1,
        },
    )
    return res["Attributes"]["visit_count"]


def lambda_handler(event, context):
    dynamo = Boto3Class("dynamodb").resource
    table_name = os.environ["DatabaseTable"]
    table = dynamo.Table(table_name)
    operation = event["httpMethod"]
    headers = event.get("headers", {})
    cookies = headers.get("Cookie")
    cookie_dict = {}
    if cookies:
        cookie_dict = {
            k.strip(): v.strip()
            for k, v in (cookie.split("=") for cookie in cookies.split(";"))
        }
    try:
        if operation == "POST":
            count = 0
            if cookie_dict.get("visited") == "true":
                count = get_visit_count(table)
            else:
                count = increment_visit_count(table)


            return {
                "statusCode": 200,
                "body": json.dumps({"visitCount": str(count)}),
                "headers": {
                    "Content-Type": "application/json",
                    "Set-Cookie": "visited=true; Max-Age=1707109200; Path=/",
                    "Access-Control-Allow-Origin": "*",
                },
            }
        else:
            return {
                "statusCode": 400,
                "body": json.dumps({'message': "Unsupported method call"}),
                "headers": {
                    "Content-Type": "application/json",
                },
            }
    except Exception as e:
        print(e)
        return {
            "statusCode": 500
        }
