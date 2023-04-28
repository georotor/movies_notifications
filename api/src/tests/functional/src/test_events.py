import pytest
from http import HTTPStatus
from uuid import uuid4

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'json, status',
    [
        (({
            "template_id": "1fa11f14-1111-4111-b1fc-1c111f11afa1",
            "event": "registered",
            "type": "email",
            "users": [str(uuid4())],
            "data": {}
        }), HTTPStatus.CREATED),
        (({
            "event": "registered",
            "type": "email",
            "users": [str(uuid4())],
            "data": {}
        }), HTTPStatus.CREATED),
        (({
            "event": "like",
            "type": "email",
            "users": [str(uuid4())],
            "data": {}
        }), HTTPStatus.UNPROCESSABLE_ENTITY),
        (({
            "type": "email",
            "users": [str(uuid4())],
            "data": {}
        }), HTTPStatus.BAD_REQUEST),
        (({
            "event": "registered",
            "type": "sms",
            "users": [str(uuid4())],
            "data": {}
        }), HTTPStatus.UNPROCESSABLE_ENTITY),
        (({
            "event": "registered",
            "type": "email",
            "users": [],
            "data": {}
        }), HTTPStatus.UNPROCESSABLE_ENTITY),
        (({
            "event": "registered",
            "type": "email",
            "users": ['1111'],
            "data": {}
        }), HTTPStatus.UNPROCESSABLE_ENTITY),
        (({
            "template_id": "1fa11f14",
            "type": "email",
            "users": [str(uuid4())],
            "data": {}
        }), HTTPStatus.BAD_REQUEST),
        (({
            "template_id": "1fa11f14-1111-4111-b1fc-1c1999999999",
            "type": "email",
            "users": [str(uuid4())],
            "data": {}
        }), HTTPStatus.BAD_REQUEST),
    ]
)
async def test_notification_create(make_json_request, json, status):
    url = '/api/v1/notifications/'
    response = await make_json_request(url=url, json=json, method='POST')
    assert response.status == status
