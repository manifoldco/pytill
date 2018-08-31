# pylint: disable=too-many-arguments
# -*- coding: utf-8 -*-

"""Main module."""
import os

import requests

TILL_USERNAME = os.getenv("USERNAME")
TILL_API_KEY = os.getenv("API_KEY")
TILL_SEND_URL = "https://platform.tillmobile.com/api/send?username={}&api_key={}"
TILL_RESULTS_URL = "https://platform.tillmobile.com/api/results"
TILL_RESULT_URL = "https://platform.tillmobile.com/api/results/{}/"
TILL_STATS_URL = "https://platform.tillmobile.com/api/stats/"
TILL_STAT_URL = "https://platform.tillmobile.com/api/stats/{}/"


def send_message(numbers, text, tag=None, voice=False):
    """Send a message with till.

    Args:
        numbers (list): List of numbers to send message to.
        text (str): Message to send.
        tag (:obj:`str`, optional): Tag to tag the project with. Defaults to None.
        voice (:obj:`bool`, optional): Whether or not to send message as boice. Defaults to None.

    Returns:
        dict: Data relating to monitoring the message sent:
        .. codeblock:: python
            {
                'stats_url': param1,
                'results_url': param2,
                'project_launch_guid': param3
            }

    Raises:
        HTTPError: For various reasons due to misconfiguration or insuffecient plan.

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
            TILL_USERNAME,
            TILL_API_KEY
        ),
        json=msg
    )

    resp.raise_for_status()
    return resp.json()


def make_question(text, tag, webhook, responses=None, conclude_on=None):
    """Make a question to ask.

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

    Note that asking a question is how we open two-way communicate in Till
    so this is also how you intiate listening to responses to a sms number with Till

    Args:
        numbers (list): List of numbers to send questions to.
        questions (list): List of questions to send.
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
    
    Example:
        >>> question = pytill.make_question('How cool is Till mobile?', 'my-question', 'my.webhook/listens/here')
        >>> pytill.send_question(['19024441111', '16139094888'], [question],  'my-project')

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
            TILL_USERNAME,
            TILL_API_KEY
        ),
        json=question_payload
    )

    resp.raise_for_status()
    return resp.json()


def get_results(question_tag=None, project_tag=None, project_launch_guid=None,
                participant_guid=None):
    """ Get results for questions asked
    
    Args:
        question_tag (:obj:`str`, optional): Tag from question to retreive on. Defaults to None.
        project_tag (:obj:`str`, optional): Tag from project (ie. list of questions to retreive on. Defaults to None.
        project_launch_guid (:obj:`str`, optional): Project guid to retreive on. Defaults to None.
        participant_guid (:obj:`str`, optional): Participant guid (ie. person/number) to retreive on. Defaults to None.

    Example:
        >>> pytill.get_results(question_tag='my-question')
        {'meta': {'limit': 20, 'next': None, 'offset': 0, 'previous': None, 'total_count': 1}, 'objects': [{'created': '2018-08-27T19:07:35.423855', 'guid': '252cd98f-5969-44c9-a955-7bb54e6f0d19', 'origin_phone_number': '+16508668969', 'participant_guid': '883c8f57-74b9-43cb-bb72-c7634b97651a', 'participant_phone_number': '+19024000158', 'project_launch_guid': '80262aea-a77e-4a0c-911f-23b959aea6da', 'project_launch_participant_guid': '8a23ee27-4841-4f2b-83d5-2a59a05825b8', 'project_tag': 'my-project', 'question_display_order': '0', 'question_guid': '8c8c168f-87d5-454d-8bae-09781312c097', 'question_tag': 'my-question', 'question_text': 'How cool is Till mobile?', 'result_answer': 'really cool!', 'result_guid': '252cd98f-5969-44c9-a955-7bb54e6f0d19', 'result_response': 'really cool!', 'result_timestamp': '2018-08-27T19:07:35.423855', 'updated': '2018-08-27T19:07:35.423884'}]}
    
    """
    query = {
        'username': TILL_USERNAME,
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
    """Get single result from result guid retreived in a ``get_results`` call"""
    query = {
        'username': TILL_USERNAME,
        'api_key': TILL_API_KEY
    }
    resp = requests.get(TILL_RESULT_URL.format(result_guid), params=query)
    resp.raise_for_status()
    return resp.json()


def get_stats(project_tag=None):
    """Get status of your Till usage. This can be broken down by project_tag."""
    query = {
        'username': TILL_USERNAME,
        'api_key': TILL_API_KEY
    }
    if project_tag:
        query['project_tag'] = project_tag

    resp = requests.get(TILL_STATS_URL, params=query)
    resp.raise_for_status()
    return resp.json()


def get_stat(project_launch_guid):
    """Get particulat status for a project_launch_guid"""
    query = {
        'username': TILL_USERNAME,
        'api_key': TILL_API_KEY
    }
    resp = requests.get(TILL_STAT_URL.format(project_launch_guid), params=query)
    resp.raise_for_status()
    return resp.json()
