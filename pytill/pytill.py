# pylint: disable=too-many-arguments
# -*- coding: utf-8 -*-

"""Main module."""
import os

import requests

TILL_UESERNAME = os.getenv("USERNAME")
TILL_API_KEY = os.getenv("API_KEY")
TILL_SEND_URL = "https://platform.tillmobile.com/api/send?username={}&api_key={}"
TILL_RESULTS_URL = "https://platform.tillmobile.com/api/results"
TILL_RESULT_URL = "https://platform.tillmobile.com/api/results/{}/"
TILL_STATS_URL = "https://platform.tillmobile.com/api/stats/"
TILL_STAT_URL = "https://platform.tillmobile.com/api/stats/{}/"


def send_message(numbers, text, tag=None, voice=False):
    """Send a message with till

    Args:
        numbers (list): List of numbers to send message to.

        text (str): Message to send.

        tag (:obj:`str`, optional): Tag to tag the project with. Defaults to None.

        voice (:obj:`bool`, optional): Whether or not to send message as boice. Defaults to None.

    Raises:
        HTTPError: For various reasons due to misconfiguration or insuffecient plan.

    Returns:
        dict: Data relating to monitoring the message sent:
            {
                'stats_url': param1,
                'results_url': param2,
                'project_launch_guid': param3
            }

    Examples:
        Send a voice message with tag greeting to multiple people.
 
        >>> resp = pytill.send_message(
            ['19021231234', '19024564567'],
            text='Hi!', tag='Greeting', voice=True)
        {'stats_url': param1, 'results_url': param2, 'project_launch_guid': param3}
    """
    msg = {
        'phone': numbers,
        'text': text
    }

    if voice:
        msg['method'] = "VOICE"

    if tag:
        msg['tag'] = tag

    resp = requests.post(
        TILL_SEND_URL.format(
            TILL_UESERNAME,
            TILL_API_KEY
        ),
        json=msg
    )

    resp.raise_for_status()
    return resp.json()


def make_question(text, tag, webhook, responses=None, conclude_on=None):
    """Make a question to ask 

    Args:
        text (str): Question to ask.

        tag (str): Question tag for retrieving results.

        webhook (str): Webhook to listen for results on.

        responses (:obj:`list`, optional): List of responses to provide. Defaults to None.

        conclude_on (:obj:`str`, optional): Response the question should conclude on. Defaults to None.

    Returns:
        dict: Question to be asked
    
    Examples:
        >>> question = pytill.make_question(
            "This is my cool question?", "cool-q-1", "sweet-web-hook-bro",
            responses=["yes", "no"], conclude_on="Thanks for answering."
        )
    """
    question = {
        "text": text,
        "tag": tag,
        "webhook": webhook
    }
    if conclude_on:
        question["conclude_on"] = conclude_on

    if responses:
        question["responses"] = responses
    return question


def send_question(numbers, questions, tag, introduction=None, conclusion=None, voice=False):
    """Send questions to ask
    Args:
        numbers (list): List of numbers to send questions to.

        numbers (list): List of questions to send.

        tag (str): Project tag for retrieving results for various questions.

        introduction (:obj:`str`, optional): Optional introduction to question(s). Defaults to None.

        conclusion (:obj:`str`, optional): Optional conclusion to question(s). Defaults to None.
        
        voice (:obj:`bool`, optional): Whether or not to ask the questions via voice. Defaults to None.

    Returns:
        dict: Data relating to monitoring the question sent:
            {
                'stats_url': param1,
                'results_url': param2,
                'project_launch_guid': param3
            }
    """
    question_payload = {
        "tag": tag,
        "phone": numbers,
        "questions": questions
    }
    if introduction:
        question_payload["introduction"] = introduction

    if conclusion:
        question_payload["conclusion"] = conclusion

    if voice:
        question_payload["method"] = "VOICE"

    resp = requests.post(
        TILL_SEND_URL.format(
            TILL_UESERNAME,
            TILL_API_KEY
        ),
        json=question_payload
    )

    resp.raise_for_status()
    return resp.json()


def get_results(question_tag=None, project_tag=None, project_launch_guid=None,
                participant_guid=None):
    """ Get results: mimics the Till API see Till for documentation for more details """
    query = {
        'username': TILL_UESERNAME,
        'api_key': TILL_API_KEY
    }
    if question_tag:
        query['question_tag'] = question_tag
    if project_tag:
        query['project_tag'] = project_tag
    if project_launch_guid:
        query['project_launch_guid'] = project_launch_guid
    if participant_guid:
        query['participant_guid'] = participant_guid

    resp = requests.get(TILL_RESULTS_URL, params=query)
    resp.raise_for_status()
    return resp.json()


def get_result(result_guid):
    """ Get result: mimics the Till API see Till for documentation for more details"""
    query = {
        'username': TILL_UESERNAME,
        'api_key': TILL_API_KEY
    }
    resp = requests.get(TILL_RESULT_URL.format(result_guid), params=query)
    resp.raise_for_status()
    return resp.json()


def get_stats(project_tag=None):
    """Get statuses: mimics the Till API see Till for documentation for more details"""
    query = {
        'username': TILL_UESERNAME,
        'api_key': TILL_API_KEY
    }
    if project_tag:
        query['project_tag'] = project_tag

    resp = requests.get(TILL_STATS_URL, params=query)
    resp.raise_for_status()
    return resp.json()


def get_stat(project_launch_guid):
    """Get status: mimics the Till API see Till for documentation for more details"""
    query = {
        'username': TILL_UESERNAME,
        'api_key': TILL_API_KEY
    }
    resp = requests.get(TILL_STAT_URL.format(project_launch_guid), params=query)
    resp.raise_for_status()
    return resp.json()
