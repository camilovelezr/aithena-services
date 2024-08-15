"""Pytest configuration."""
import pytest



@pytest.fixture
def user_message():
    message = {'role': 'user', 'content': 'Why is the sky blue?'}
    return message