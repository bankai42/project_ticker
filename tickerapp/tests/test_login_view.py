from django.test import Client
import pytest
from django.urls import reverse
from conftest import TESTPASS

@pytest.fixture
def login_url():
    return reverse('login')


def test_login_get(login_url):
    response = Client().get(login_url)
    assert response.status_code == 200
    
    

@pytest.mark.django_db
def test_login_redirect_auth(auth_client, login_url):
    response = auth_client.get(login_url)
    assert response.status_code == 302
    assert response.url == reverse('home')


@pytest.mark.django_db
def test_login_success(test_user, login_url):
    data = {
        'username': test_user.username,
        'password': TESTPASS
        }
    response = Client().post(login_url, data=data)
    assert response.status_code == 302
    assert response.url == reverse('home')


@pytest.mark.django_db
def test_login_failure(test_user, login_url):
    data = {
        'username': 'wronguser',
        'password': 'wrongpass'
        }
    response = Client().post(login_url, data=data)
    assert response.status_code == 200
    assert 'Username or password does not exists' in response.content.decode()