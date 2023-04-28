import pytest
from http import HTTPStatus
from uuid import uuid4

pytestmark = pytest.mark.asyncio

SCHEDULED_ID = str(uuid4())


@pytest.mark.parametrize(
    'json, status',
    [
        (({
            "name": "string",
            "timestamp_start": 121313,
            "cron": "*/1 * * * *",
            "type": "email",
            "template_id": "1fa11f14-1111-4111-b1fc-1c111f11afa1",
            "users": [str(uuid4())],
            "data": {},
            "enabled": True
        }), HTTPStatus.CREATED),
        (({
            "name": "string",
            "timestamp_start": 121313,
            "cron": "*/1 * * * *",
            "type": "email",
            "template_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "users": [str(uuid4())],
            "data": {},
            "enabled": True
        }), HTTPStatus.BAD_REQUEST),
        (({
            "name": "string",
            "timestamp_start": 121313,
            "cron": "ss * * * *",
            "type": "email",
            "template_id": "1fa11f14-1111-4111-b1fc-1c111f11afa1",
            "users": [str(uuid4())],
            "data": {},
            "enabled": True
        }), HTTPStatus.BAD_REQUEST),
        (({
            "name": "string",
            "timestamp_start": 121313,
            "type": "email",
            "template_id": "1fa11f14-1111-4111-b1fc-1c111f11afa1",
            "users": [str(uuid4())],
            "data": {},
            "enabled": True
        }), HTTPStatus.CREATED),
        (({
            "name": "string",
            "cron": "*/1 * * * *",
            "type": "email",
            "template_id": "1fa11f14-1111-4111-b1fc-1c111f11afa1",
            "users": [str(uuid4())],
            "data": {},
            "enabled": True
        }), HTTPStatus.CREATED),
        (({
            "name": "string",
            "cron": "*/1 * * * *",
            "type": "sms",
            "template_id": "1fa11f14-1111-4111-b1fc-1c111f11afa1",
            "users": [str(uuid4())],
            "data": {},
            "enabled": True
        }), HTTPStatus.UNPROCESSABLE_ENTITY),
        (({
            "name": "string",
            "cron": "*/1 * * * *",
            "type": "email",
            "template_id": "11111",
            "users": [str(uuid4())],
            "data": {},
            "enabled": True
        }), HTTPStatus.UNPROCESSABLE_ENTITY),
        (({
            "name": "string",
            "cron": "*/1 * * * *",
            "type": "email",
            "template_id": "1fa11f14-1111-4111-b1fc-1c111f11afa1",
            "users": [],
            "data": {},
            "enabled": True
        }), HTTPStatus.UNPROCESSABLE_ENTITY),
        (({
            "name": "string",
            "cron": "*/1 * * * *",
            "type": "email",
            "template_id": "1fa11f14-1111-4111-b1fc-1c111f11afa1",
            "users": None,
            "data": {},
            "enabled": True
        }), HTTPStatus.UNPROCESSABLE_ENTITY),
        (({
            "name": "string",
            "cron": "*/1 * * * *",
            "type": "email",
            "template_id": "1fa11f14-1111-4111-b1fc-1c111f11afa1",
            "users": [str(uuid4())],
            "data": 111,
            "enabled": True
        }), HTTPStatus.UNPROCESSABLE_ENTITY),
        (({
            "name": "string",
            "cron": "*/1 * * * *",
            "type": "email",
            "template_id": "1fa11f14-1111-4111-b1fc-1c111f11afa1",
            "users": [str(uuid4())],
            "data": {},
            "enabled": 111
        }), HTTPStatus.UNPROCESSABLE_ENTITY),
        (({
            "scheduled_id": "sss",
            "name": "string",
            "cron": "*/1 * * * *",
            "type": "email",
            "template_id": "1fa11f14-1111-4111-b1fc-1c111f11afa1",
            "users": [str(uuid4())],
            "data": {},
            "enabled": True
        }), HTTPStatus.UNPROCESSABLE_ENTITY),
        (({
            "scheduled_id": SCHEDULED_ID,
            "name": "string",
            "cron": "*/1 * * * *",
            "type": "email",
            "template_id": "1fa11f14-1111-4111-b1fc-1c111f11afa1",
            "users": [str(uuid4())],
            "data": {},
            "enabled": True
        }), HTTPStatus.CREATED),
    ]
)
async def test_schedulers_create(make_json_request, json, status):
    url = '/api/v1/schedulers/'
    response = await make_json_request(url=url, json=json, method='POST')
    print(json)
    assert response.status == status


async def test_schedulers_get(make_json_request):
    url = f'/api/v1/schedulers/{SCHEDULED_ID}'

    response = await make_json_request(url=url, method='GET')

    assert response.status == HTTPStatus.OK
    assert isinstance(response.body, dict)


async def test_schedulers_list(make_json_request):
    url = '/api/v1/schedulers/'

    response = await make_json_request(url=url, method='GET')

    assert response.status == HTTPStatus.OK
    assert isinstance(response.body, list)


@pytest.mark.parametrize(
    'json, status',
    [
        (({
            "name": "string",
            "timestamp_start": 121313,
            "cron": "*/1 * * * *",
            "type": "email",
            "template_id": "1fa11f14-1111-4111-b1fc-1c111f11afa1",
            "users": [str(uuid4())],
            "data": {},
            "enabled": True
        }), HTTPStatus.BAD_REQUEST),
        (({
            "scheduled_id": SCHEDULED_ID,
            "name": "string",
            "timestamp_start": 121313,
            "cron": "*/1 * * * *",
            "type": "email",
            "template_id": "1fa11f14-1111-4111-b1fc-1c111f11afa1",
            "users": [str(uuid4())],
            "data": {},
            "enabled": True
        }), HTTPStatus.OK),
        (({
            "scheduled_id": SCHEDULED_ID,
            "name": "string",
            "timestamp_start": "qwer",
            "cron": "*/1 * * * *",
            "type": "email",
            "template_id": "1fa11f14-1111-4111-b1fc-1c111f11afa1",
            "users": [str(uuid4())],
            "data": {},
            "enabled": True
        }), HTTPStatus.UNPROCESSABLE_ENTITY),
        (({
            "scheduled_id": SCHEDULED_ID,
            "name": "string",
            "timestamp_start": 123,
            "cron": "1111 * * * *",
            "type": "email",
            "template_id": "1fa11f14-1111-4111-b1fc-1c111f11afa1",
            "users": [str(uuid4())],
            "data": {},
            "enabled": True
        }), HTTPStatus.BAD_REQUEST),
        (({
            "scheduled_id": SCHEDULED_ID,
            "name": "string",
            "timestamp_start": 123,
            "cron": "*/1 * * * *",
            "type": "email",
            "template_id": "1fa11f14-1111-4111-b1fc-111111111f11",
            "users": [str(uuid4())],
            "data": {},
            "enabled": True
        }), HTTPStatus.BAD_REQUEST),
        (({
            "scheduled_id": SCHEDULED_ID,
            "name": "string",
            "timestamp_start": 123,
            "cron": "*/1 * * * *",
            "type": "email",
            "template_id": "1111",
            "users": [str(uuid4())],
            "data": {},
            "enabled": True
        }), HTTPStatus.UNPROCESSABLE_ENTITY),
        (({
            "scheduled_id": SCHEDULED_ID,
            "name": "string",
            "timestamp_start": 121313,
            "cron": "*/1 * * * *",
            "type": "email",
            "template_id": "1fa11f14-1111-4111-b1fc-1c111f11afa1",
            "users": [],
            "data": {},
            "enabled": True
        }), HTTPStatus.UNPROCESSABLE_ENTITY),
        (({
            "scheduled_id": SCHEDULED_ID,
            "name": "string",
            "timestamp_start": 121313,
            "cron": "*/1 * * * *",
            "type": "email",
            "template_id": "1fa11f14-1111-4111-b1fc-1c111f11afa1",
            "users": 123,
            "data": {},
            "enabled": True
        }), HTTPStatus.UNPROCESSABLE_ENTITY),
        (({
            "scheduled_id": SCHEDULED_ID,
            "name": "string",
            "timestamp_start": 121313,
            "cron": "*/1 * * * *",
            "type": "email",
            "template_id": "1fa11f14-1111-4111-b1fc-1c111f11afa1",
            "users": [str(uuid4())],
            "data": {},
            "enabled": 123
        }), HTTPStatus.UNPROCESSABLE_ENTITY),
    ]
)
async def test_schedulers_update(make_json_request, json, status):
    url = '/api/v1/schedulers/'
    response = await make_json_request(url=url, json=json, method='PUT')
    assert response.status == status


async def test_schedulers_delete(make_json_request):
    url = f'/api/v1/schedulers/{SCHEDULED_ID}'
    response = await make_json_request(url=url, method='DELETE')
    assert response.status == HTTPStatus.OK

    response = await make_json_request(url=url, method='GET')
    assert response.status == HTTPStatus.NOT_FOUND
