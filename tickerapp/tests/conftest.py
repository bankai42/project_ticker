import pytest
from django.contrib.auth.models import User
from django.test import Client

TESTPASS = 'testpassword'


@pytest.fixture
def test_user():
    test_user = User.objects.create_user(username='testuser', password=TESTPASS)
    return test_user


@pytest.fixture
def auth_client(test_user):
    client = Client()
    client.login(username=test_user.username, password=TESTPASS)
    return client