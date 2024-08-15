"""Pytest configuration."""
import pytest
import os

@pytest.fixture
def user_message():
    message = {'role': 'user', 'content': 'Why is the sky blue?'}
    return message
