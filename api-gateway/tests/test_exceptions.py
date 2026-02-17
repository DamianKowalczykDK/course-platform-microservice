from unittest.mock import MagicMock
from webapp.services.exceptions import (
    ServerException,
    NotFoundException,
    raise_for_status,
    extract_message,
    ValidationException
)
import httpx
import pytest


def test_extract_message() -> None:
    mock_resp = MagicMock(spec=httpx.Response)
    mock_resp.json.return_value = {
        "message": "Test",
        "error": "error",
        "details": ["Test1"]
    }
    mock_resp.status_code = 404
    message, error_code, details = extract_message(mock_resp)

    assert message == "Test"
    assert error_code == "error"
    assert details == ["Test1"]

def test_extract_message_value_error() -> None:
    mock_resp = MagicMock(spec=httpx.Response)
    mock_resp.text = "raw response text"

    mock_resp.json.side_effect = ValueError
    message, error_code, details = extract_message(mock_resp)
    assert message == "raw response text"
    assert details == []


def test_raise_for_status_not_found_exception() -> None:
    mock_resp = MagicMock(spec=httpx.Response)
    mock_resp.json.return_value = {"message": "User not found"}
    mock_resp.status_code = 404

    with pytest.raises(NotFoundException) as e:
        raise_for_status(mock_resp)
    assert "User not found" in str(e)

def test_raise_for_status_server_exception() -> None:
    mock_resp = MagicMock(spec=httpx.Response)
    mock_resp.json.return_value = {"message": "server_error", "details": ["Test"]}
    mock_resp.status_code = 500

    with pytest.raises(ServerException) as e:
        raise_for_status(mock_resp)

    result = e.value
    assert result.message == "server_error"

def test_raise_for_status_validation_exception_if_error_validation_error() -> None:
    mock_resp = MagicMock(spec=httpx.Response)
    mock_resp.json.return_value = {
        "message": "Invalid input",
        "error": "validation_error",
        "details": ["Test", "Test2"]}
    mock_resp.status_code = 400

    with pytest.raises(ValidationException) as e:
        raise_for_status(mock_resp)

    result = e.value

    assert result.error_code == "validation_error"
    assert result.details[1] == "Test2"

def test_raise_for_status_validation_exception() -> None:
    mock_resp = MagicMock(spec=httpx.Response)
    mock_resp.json.return_value = {
        "message": "test_error",
      }
    mock_resp.status_code = 400

    with pytest.raises(ValidationException) as e:
        raise_for_status(mock_resp)

    result = e.value

    assert result.message == "test_error"