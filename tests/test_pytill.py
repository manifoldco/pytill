#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pytill` package."""
from unittest.mock import Mock

import pytest
import requests

from pytill import pytill

GUID = 'cool_guid'
STATS_URL = 'sweet-url/dog'
RESULTS_URL = 'nice-results/bro'

@pytest.fixture
def send_success(monkeypatch):
    def mock_post(url, data=None, json=None, **kwargs):
        msg_response = {
            'project_launch_guid': GUID,
            'stats_url': STATS_URL,
            'results_url': RESULTS_URL
        }
        mock = Mock()
        mock.request_for_status = Mock()
        mock.json = Mock(return_value=msg_response)
        return mock
    monkeypatch.setattr(requests, 'post', mock_post)

@pytest.fixture
def send_failure(monkeypatch):
    def mock_post(url, data=None, json=None, **kwargs):
        def mock_raise():
            raise requests.HTTPError('oops')
        mock = Mock()
        mock.request_for_status = Mock(side_effect=mock_raise())
        return mock

    monkeypatch.setattr(requests, 'post', mock_post)

@pytest.fixture
def get_failure(monkeypatch):
    def mock_get(url, params=None, **kwargs):
        def mock_raise():
            raise requests.HTTPError('oops')
        mock = Mock()
        mock.request_for_status = Mock(side_effect=mock_raise())
        return mock

    monkeypatch.setattr(requests, 'get', mock_get)

@pytest.fixture
def get_result(monkeypatch):
    def mock_get(url, params=None, **kwargs):
        msg_response = {'something': 'somethingelse'}
        mock = Mock()
        mock.request_for_status = Mock()
        mock.json = Mock(return_value=msg_response)
        return mock
    monkeypatch.setattr(requests, 'get', mock_get)

def test_send_message(send_success):
    expected_guid = GUID
    r = pytill.send_message(['19021234567'],
        'Hi how are you? Its dom I am doing a test',
        tag='Greeting', voice=True
    )
    assert expected_guid == r['project_launch_guid']
       
def test_send_message_raises(send_failure):
    with pytest.raises(requests.HTTPError):
        pytill.send_message(['19021234567'], 'Hi how are you? Its dom I am doing a test')

def test_make_question():
    expected_question =  {
          'conclude_on': 'Thanks for answering.',
          'responses': ['yes', 'no'],
          'tag': 'cool-q-1',
          'text': 'This is my cool question?',
          'webhook': 'sweet-web-hook-bro'
    }
    question = pytill.make_question(
        "This is my cool question?", "cool-q-1", "sweet-web-hook-bro",
         responses=["yes", "no"], conclude_on="Thanks for answering."
    )
    assert expected_question == question

def test_send_question(send_success):
    expected_response = {
        'project_launch_guid': GUID,
        'stats_url': STATS_URL,
        'results_url': RESULTS_URL
    }
    questions = [pytill.make_question(
        'How are you?', "how-r-u", "how-r-u-webhook.com",
        responses=["Good", "Bad"], conclude_on="Thanks"
    )]
    r = pytill.send_question(['19021234567'],
        questions,
        "my-project-tag",
        introduction="Hey can I ask you a question",
        conclusion="Thanks for letting me ask you a question"
    )
    assert expected_response == r
      
def test_send_question_raises(send_failure):
    with pytest.raises(requests.HTTPError):
        questions = [pytill.make_question('How are you?', "how-r-u", "how-r-u-webhook.com")]
        pytill.send_question(['190212345678'], 'greetings-project', questions)

def test_get_results(get_result):
    expected_response = {'something': 'somethingelse'}
    r = pytill.get_results()
    assert expected_response == r

def test_get_results_raises(get_failure):
    with pytest.raises(requests.HTTPError):
        pytill.get_results()

def test_get_result(get_result):
    expected_response = {'something': 'somethingelse'}
    r = pytill.get_result('some-guid')
    assert expected_response == r

def test_get_result_raises(get_failure):
    with pytest.raises(requests.HTTPError):
        pytill.get_results()

def test_get_stats(get_result):
    expected_response = {'something': 'somethingelse'}
    r = pytill.get_stats()
    assert expected_response == r

def test_get_stats_raises(get_failure):
    with pytest.raises(requests.HTTPError):
        pytill.get_stats()

def test_get_stat(get_result):
    expected_response = {'something': 'somethingelse'}
    r = pytill.get_stat('some-guid')
    assert expected_response == r

def test_get_stat_raises(get_failure):
    with pytest.raises(requests.HTTPError):
        pytill.get_stat('some-guid')
