import json
import os
from moto import mock_dynamodb
import pytest
from unittest.mock import patch
import boto3
from src.visit_count.handler import lambda_handler

MOCK_TABLE_NAME = "mock-table-name"


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture
def dynamodb(aws_credentials):
    with mock_dynamodb():
        yield boto3.resource("dynamodb")


@pytest.fixture
def mock_table(dynamodb):
    dynamodb.create_table(
        TableName=MOCK_TABLE_NAME,
        KeySchema=[
            {"AttributeName": "pk", "KeyType": "HASH"},
            {"AttributeName": "sk", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "pk", "AttributeType": "S"},
            {"AttributeName": "sk", "AttributeType": "S"},
        ],
        BillingMode="PAY_PER_REQUEST",
    )
    yield dynamodb.Table(MOCK_TABLE_NAME)


@pytest.fixture
def mock_table_with_visit_count_in_place(mock_table):
    mock_table.put_item(Item={"pk": "visitors", "sk": "visitors", "visit_count": 10})
    yield mock_table


@patch.dict(os.environ, {"DatabaseTable": MOCK_TABLE_NAME})
def test_post_visitor_count_handler(mock_table):
    with open("./tests/events/api_gw_post_visitCount.json") as f:
        event = json.load(f)

    expected_data = {"visitCount": "1"}

    res = lambda_handler(event, "")
    data = json.loads(res["body"])
    assert data == expected_data


@patch.dict(os.environ, {"DatabaseTable": MOCK_TABLE_NAME})
def test_get_visit_count_handler(mock_table):
    with open("./tests/events/api_gw_get_visitCount.json") as f:
        event = json.load(f)

    expected_data = {"message": "Unsupported method call"}

    res = lambda_handler(event, "")
    data = json.loads(res["body"])
    assert data == expected_data


@patch.dict(os.environ, {"DatabaseTable": MOCK_TABLE_NAME})
def test_delete_visit_count_handler(mock_table):
    with open("./tests/events/api_gw_delete_visitCount.json") as f:
        event = json.load(f)

    expected_data = {"message": "Unsupported method call"}

    res = lambda_handler(event, "")
    data = json.loads(res["body"])
    assert data == expected_data


@patch.dict(os.environ, {"DatabaseTable": MOCK_TABLE_NAME})
def test_post_visit_count_with_visited_cookie_handler(
    mock_table_with_visit_count_in_place,
):
    with open("./tests/events/api_gw_post_visitCount.json") as f:
        event = json.load(f)
        event["headers"]["Cookie"] = "visited=true; Max-Age=1707109200; Path=/"

    expected_data = {"visitCount": "10"}

    res = lambda_handler(event, "")
    data = json.loads(res["body"])
    assert data == expected_data
