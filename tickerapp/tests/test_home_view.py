import pytest
from django.test import Client
from django.urls import reverse
from conftest import TESTPASS
from tickerapp.forms import TickerTextForm
from tickerapp.models import Ticker
from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def home_url():
    return reverse('home')


@pytest.fixture
def test_ticker(test_user):
    ticker = Ticker.objects.create(owner=test_user, text='Test Text', filename='testfilename', video_file='videos/testvideo.avi')
    return ticker
    
    
def test_home_get_unauth(home_url):
    response = Client().get(home_url)
    assert response.status_code == 200
    assert not response.context['tickers']
    assert isinstance(response.context['form'], TickerTextForm)


@pytest.mark.django_db
def test_home_get_auth(home_url, auth_client, test_ticker):
    response = auth_client.get(home_url)
    assert response.status_code == 200
    assert response.context['tickers']
    assert isinstance(response.context['form'], TickerTextForm)
    

@pytest.mark.django_db
def test_home_post_auth(home_url, auth_client, test_user):
    data = {
        'text': 'Test Text',
        'filename': 'testfilename',
    }
    response = auth_client.post(home_url, data=data)
    ticker = Ticker.objects.latest('timestamp')
    assert ticker
    assert ticker.owner == test_user
    assert ticker.text == data['text']
    assert ticker.filename == data['filename']
    assert ticker.video_file
    assert response.status_code == 302
    assert response.url == reverse('home')
    

@pytest.mark.django_db
def test_home_post_auth_create_download(home_url, auth_client, test_user):
    data = {
        'text': 'Test Text',
        'filename': 'testfilename',
        'create_and_download': True,
    }
    response = auth_client.post(home_url, data=data)
    ticker = Ticker.objects.latest('timestamp')
    assert ticker
    assert ticker.owner == test_user
    assert ticker.text == data['text']
    assert ticker.filename == data['filename']
    assert ticker.video_file
    assert response.status_code == 302
    assert response.url == reverse('download', kwargs={'pk': ticker.id})
    
    
@pytest.mark.django_db
def test_home_post_unauth_create_download(home_url):
    data = {
        'text': 'Test Text',
        'filename': 'testfilename',
        'create_and_download': True,
    }
    response = Client().post(home_url, data=data)
    ticker = Ticker.objects.latest('timestamp')
    assert ticker
    assert ticker.owner == None
    assert ticker.text == data['text']
    assert ticker.filename == data['filename']
    assert ticker.video_file
    assert response.status_code == 302
    assert response.url == reverse('download', kwargs={'pk': ticker.id})