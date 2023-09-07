
from fastapi.testclient import TestClient
import pytest
from .main import app
from .main import text_to_image

client = TestClient(app)

@pytest.mark.asyncio
async def test_text_to_image(mocker):

    mock_requests_post = mocker.patch('requests.post')
    expected_response = mocker.MagicMock()
    expected_response.json.return_value = {
        'artifacts': [{'base64': 'mocked_base64_image_data'}]
    }
    expected_response.content = b'mocked_content_data'

    mock_requests_post.return_value = expected_response

    response = await text_to_image('Text prompt')

    assert response.status_code == 200
    assert response.body == b'mocked_base64_image_data'

