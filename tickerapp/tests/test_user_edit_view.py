import pytest
from django.urls import reverse
from tickerapp.forms import UserForm


@pytest.fixture
def edit_profile_url(test_user):
    return reverse('edit_profile', kwargs={'pk': test_user.id})


@pytest.mark.django_db
def test_userEdit_get_request(auth_client, edit_profile_url):
    response = auth_client.get(edit_profile_url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], UserForm)


@pytest.mark.django_db
def test_userEdit_post_request(test_user, auth_client, edit_profile_url):
    data = {
        'username': 'newusername',
        'first_name': 'New',
        'last_name': 'User',
        'email': 'newuser@example.com'
    }
    response = auth_client.post(edit_profile_url, data)
    assert response.status_code == 302
    assert response.url == reverse('profile', kwargs={'pk': test_user.id})

    test_user.refresh_from_db()
    assert test_user.username == 'newusername'
    assert test_user.first_name == 'New'
    assert test_user.last_name == 'User'
    assert test_user.email == 'newuser@example.com'


@pytest.mark.django_db
def test_userEdit_post_request_invalid_data(auth_client, edit_profile_url):   
    data = {
        'username': '',
        'first_name': 'New',
        'last_name': 'User',
        'email': 'newuser@example.com'
    }
    response = auth_client.post(edit_profile_url, data)
    assert response.status_code == 200
    assert 'This field is required.' in str(response.context['form'].errors)
