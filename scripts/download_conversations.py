import os
import requests
import json
from pprint import pprint

def get_conversation_batch(url):
    """
    Get a batch of conversations from the intercom API
    """
    return requests.get(
        url, 
        headers={
            'Accept': 'application/json',
        },
        auth=(
            os.getenv("INTERCOM_APP_ID"),
            os.getenv("INTERCOM_API_KEY")
        )
    ).json()


def get_conversation(conversation_id):
    """
    Get the message from a single conversation from the intercom API
    """
    return requests.get(
        'https://api.intercom.io/conversations/%s'
        '?display_as=plaintext' % conversation_id,
        headers={
            'Accept': 'application/json',
        },
        auth=(
            os.getenv("INTERCOM_APP_ID"),
            os.getenv("INTERCOM_API_KEY")
        )
    ).json()


def list_messages():
    """
    Get all user-initiated conversations from the intercom API
    """
    results = []

    url = 'https://api.intercom.io/conversations'
    i = 0
    while True:
        i += 1
        j = 0
        conversations = get_conversation_batch(url)
        for conversation in conversations.get('conversations'):
            j += 1
            print "Page: %d, Conversation: %d" % (i, j)

            conversation_id = conversation.get('id')
            conversation_data = get_conversation(conversation_id)
            conversation_parts = conversation_data.get('conversation_parts')
            messages = conversation_parts.get('conversation_parts')

            # get all user messages before our first response
            assignee = None
            message_text = []
            author_ids = []
            for message in messages:
                if message.get('author').get('type') == 'user':
                    message_text.append(message.get('body'))
                elif message.get('author').get('type') == 'admin':
                    author_ids.append(message.get('author').get('id'))

                if message.get('assigned_to'):
                    assignee = message.get('assigned_to').get('id')
                    break
            
            if message_text:
                # if no one was explicitly assigned, 
                # use the last person to respond to the conversation
                if assignee is None and author_ids:
                    assignee = author_ids[-1]

                if assignee:
                    results.append([message_text, assignee])

        url = conversations.get('pages').get('next')

        # pagination finished
        if not url:
            break

    return results


if __name__ == "__main__":
    messages = list_messages()
    json.dump(messages, open('data/messages.json', 'w'))
