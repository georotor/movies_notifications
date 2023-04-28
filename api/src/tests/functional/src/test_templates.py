import pytest
from http import HTTPStatus
from uuid import uuid4

pytestmark = pytest.mark.asyncio


async def test_templates_list(make_json_request):
    url = '/api/v1/templates/'

    response = await make_json_request(url=url, method='GET')

    assert response.status == HTTPStatus.OK
    assert len(response.body) == 1


async def test_templates_list_skip(make_json_request):
    url = '/api/v1/templates/'
    params = {'skip': 1}

    response = await make_json_request(url=url, params=params, method='GET')

    assert response.status == HTTPStatus.OK
    assert len(response.body) == 0


@pytest.mark.parametrize(
    'json, status',
    [
        (({
            "name": "string",
            "event": "registered",
            "type": "email",
            "subject": "string",
            "content": "string"
        }), HTTPStatus.BAD_REQUEST),
        (({
            "name": "string",
            "event": "ku-ku",
            "type": "email",
            "subject": "string",
            "content": "string"
        }), HTTPStatus.UNPROCESSABLE_ENTITY),
        (({
            "name": "string",
            "event": "registered",
            "type": "sms",
            "subject": "string",
            "content": "string"
        }), HTTPStatus.UNPROCESSABLE_ENTITY),
        (({
            "name": "string",
            "type": "email",
            "subject": "{{string}",
            "content": "string"
        }), HTTPStatus.BAD_REQUEST),
        (({
            "name": "string",
            "type": "email",
            "subject": "{{string}}",
            "content": "{{string}"
        }), HTTPStatus.BAD_REQUEST),
        (({
            "name": "string",
            "type": "email",
            "content": "{{string}}"
        }), HTTPStatus.BAD_REQUEST),
        (({
            "name": "string",
            "type": "email",
            "subject": "{{string}}",
            "content": "{{string}}"
        }), HTTPStatus.CREATED),
        (({
            "template_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "name": "string",
            "type": "email",
            "subject": "{{string}}",
            "content": "{{string}}"
        }), HTTPStatus.CREATED),
        (({
            "template_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "name": "string",
            "type": "email",
            "subject": "{{string}}",
            "content": "{{string}}"
        }), HTTPStatus.BAD_REQUEST),
    ]
)
async def test_template_create(make_json_request, json, status):
    url = '/api/v1/templates/'
    response = await make_json_request(url=url, json=json, method='POST')
    assert response.status == status


async def test_template_get(make_json_request):
    url = '/api/v1/templates/1fa11f14-1111-4111-b1fc-1c111f11afa1'

    response = await make_json_request(url=url, method='GET')

    assert response.status == HTTPStatus.OK
    assert isinstance(response.body, dict)


async def test_template_get_not_found(make_json_request):
    url = '/api/v1/templates/1fa11f14-1111-4111-b1fc-1c111f11afa2'
    response = await make_json_request(url=url, method='GET')
    assert response.status == HTTPStatus.NOT_FOUND


async def test_template_get_not_valid_uuid(make_json_request):
    url = '/api/v1/templates/11111'
    response = await make_json_request(url=url, method='GET')
    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    'json, status',
    [
        (({
            "template_id": "22a85f64-2222-2222-2222-2c963f66af22",
            "name": "string",
            "event": "registered",
            "type": "email",
            "subject": "string",
            "content": "string"
        }), HTTPStatus.NOT_FOUND),
        (({
            "template_id": "1fa11f14-1111-4111-b1fc-1c111f11afa1",
            "name": str(uuid4()),
            "event": "registered",
            "type": "email",
            "subject": "string",
            "content": "string"
        }), HTTPStatus.OK),
        (({
            "template_id": "1fa11f14-1111-4111-b1fc-1c111f11afa1",
            "name": "string",
            "event": "ku-ku",
            "type": "email",
            "subject": "string",
            "content": "string"
        }), HTTPStatus.UNPROCESSABLE_ENTITY),
        (({
            "template_id": "1fa11f14-1111-4111-b1fc-1c111f11afa1",
            "name": "string",
            "event": "registered",
            "type": "sms",
            "subject": "string",
            "content": "string"
        }), HTTPStatus.UNPROCESSABLE_ENTITY),
        (({
            "template_id": "1fa11f14-1111-4111-b1fc-1c111f11afa1",
            "name": "string",
            "type": "email",
            "subject": "{{string}",
            "content": "string"
        }), HTTPStatus.BAD_REQUEST),
        (({
            "template_id": "1fa11f14-1111-4111-b1fc-1c111f11afa1",
            "name": "string",
            "type": "email",
            "subject": "{{string}}",
            "content": "{{string}"
        }), HTTPStatus.BAD_REQUEST),
        (({
            "template_id": "1fa11f14-1111-4111-b1fc-1c111f11afa1",
            "name": "string",
            "type": "email",
            "content": "{{string}}"
        }), HTTPStatus.BAD_REQUEST),
    ]
)
async def test_template_update(make_json_request, json, status):
    url = '/api/v1/templates/'
    response = await make_json_request(url=url, json=json, method='PUT')
    assert response.status == status


async def test_template_delete(make_json_request):
    json = {
        "template_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "name": "string",
        "type": "email",
        "subject": "{{string}}",
        "content": "{{string}}",
    }
    url = '/api/v1/templates/'
    await make_json_request(url=url, json=json, method='POST')

    url = '/api/v1/templates/3fa85f64-5717-4562-b3fc-2c963f66afa6'
    response = await make_json_request(url=url, method='DELETE')
    assert response.status == HTTPStatus.OK

    response = await make_json_request(url=url, method='GET')
    assert response.status == HTTPStatus.NOT_FOUND
