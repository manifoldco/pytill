=====
Usage
=====

Set up a plan for till and retrieve till username and api key. This packages expects the username and api key are injected as env vars ``USERNAME`` and ``API_KEY``.

You can do this simply through manifold:

.. code-block:: bash

    manifold create -p till-project --product till --plan free # provision a free till resource
    manifold run -p till-project -- python # inject vars


.. code-block:: python

    import pytill # or from pytill import pytill

    # send a message
    pytill.send_message(['19024880000'], 'I am sending a till message isnt that cool!')

    # ask a question
    # note that asking a question is how we open two-way communicate in Till
    # so this is also how you intiate listening to responses to a sms number with Till
    question = pytill.make_question('How cool is Till mobile?', 'my-question', 'my.webhook/listens/here')
    pytill.send_question(['19024441111', '16139094888'], [question],  'my-project')

    # retrieve result
    print(pytill.get_results(question_tag='my-question'))

    # example output

    # {'meta': {'limit': 20, 'next': None, 'offset': 0, 'previous': None, 'total_count': 1}, 'objects': [{'created': '2018-08-27T19:07:35.423855', 'guid': '252cd98f-5969-44c9-a955-7bb54e6f0d19', 'origin_phone_number': '+16508668969', 'participant_guid': '883c8f57-74b9-43cb-bb72-c7634b97651a', 'participant_phone_number': '+19024000158', 'project_launch_guid': '80262aea-a77e-4a0c-911f-23b959aea6da', 'project_launch_participant_guid': '8a23ee27-4841-4f2b-83d5-2a59a05825b8', 'project_tag': 'my-project', 'question_display_order': '0', 'question_guid': '8c8c168f-87d5-454d-8bae-09781312c097', 'question_tag': 'my-question', 'question_text': 'How cool is Till mobile?', 'result_answer': 'really cool!', 'result_guid': '252cd98f-5969-44c9-a955-7bb54e6f0d19', 'result_response': 'really cool!', 'result_timestamp': '2018-08-27T19:07:35.423855', 'updated': '2018-08-27T19:07:35.423884'}]}

    # retrive stats about till usage
    print(pytill.get_stats())
