"""
IndicoService intercom webhook route
"""
from operator import itemgetter

from intercom import Conversation, Admin, Intercom
from indicoio.custom import Collection
from indicoio import IndicoError

from .handler import IndicoHandler
from ..config import (
    ASSIGNMENT_THRESHOLD, SUGGESTION_THRESHOLD, COLLECTION_NAME,
    SUGGESTOR_ID, MENTION_TEMPLATE, SECRET_MENTION_ID
)
from ..utils import LOGGER, unpack, type_check
from ..utils.message_utils import extract_messages_text


class WebhookHandler(IndicoHandler):
    @unpack("data")
    @type_check(dict)
    def _base(self, data):
        """
        Handle Intercom incoming webhook
        """
        conversation = data.get('item')
        conversation_id = conversation.get('id')
        conversation_parts = conversation.get("conversation_parts", {}).get("conversation_parts")
        assignee_id = conversation.get("assignee", {}).get("id")

        if len(conversation_parts) == 0:
            # this is a new conversation
            return self._predict(conversation_id, assignee_id=assignee_id)
        elif conversation_parts[-1].get('part_type') == "assignment":
            # this is a conversation assignment
            return self._add_data_to_collection(conversation_id, assignee_id=assignee_id)
        else:
            # this is a reply
            return self._predict(conversation_id, assignee_id=assignee_id)


    def _add_data_to_collection(self, conversation_id, assignee_id):
        """
        Add data to the collection when a conversation gets assigned
        """

        conversation = Conversation.find(id=conversation_id)
        messages = [conversation.conversation_message] + conversation.conversation_parts

        for message in messages:
            if SECRET_MENTION_ID in (message.body or ""):
                # we've already suggested an Admin, don't suggest again
                return
        
        LOGGER.info("Adding data to collections for assignee {id}".format(
            id=assignee_id
        ))

        messages = filter(
            lambda msg: not isinstance(msg.author, Admin),
            messages
        )

        message_text = extract_messages_text(messages)

        collection = Collection(COLLECTION_NAME, domain='topics')
        collection.add_data([message_text, assignee_id])

        try:
            collection.train()
        except IndicoError as e:
            pass

    def _predict(self, conversation_id, assignee_id=None):
        """
        Predict the assignee
        """
        conversation = Conversation.find(id=conversation_id)
        messages = [conversation.conversation_message] + conversation.conversation_parts

        for message in messages:
            if SECRET_MENTION_ID in (message.body or ""):
                # we've already suggested an Admin, don't suggest again
                return

        collection = Collection(COLLECTION_NAME, domain='topics')
        text = extract_messages_text(messages)
        results = collection.predict(text)

        best_prediction = sorted(results.items(), key=itemgetter(1))[-1]
        if best_prediction[1] > ASSIGNMENT_THRESHOLD:
            if assignee_id is not None:
                self._suggest_assignee(conversation, best_prediction[0])
            else:
                self._assign_assignee(conversation, best_prediction[0])

        elif best_prediction[1] > SUGGESTION_THRESHOLD:
            self._suggest_assignee(conversation, best_prediction[0])
        else:
            LOGGER.debug(
                "Prediction did not produce high enough results for conversation {id} with {results}".format(
                    id=conversation_id,
                    results=results
                )
            )

    def _suggest_assignee(self, conversation, assignee_id):
        """
        @param conversation - Intercom Conversation class object
        """
        LOGGER.debug("Suggesting assignee {a_id} for conversation {c_id}".format(
            a_id=assignee_id,
            c_id=conversation.id
        ))

        if conversation.assignee.id == assignee_id:
            # don't suggest the user that is already assigned
            return

        user = Admin.find(id=assignee_id)
        mention = MENTION_TEMPLATE.format(
            intercom_app_id=Intercom.app_id,
            user_id=user.id,
            username=user.name
        )
        conversation.reply(
            type='admin', id=SUGGESTOR_ID,
            message_type='note', body="This seems fit for {mention}".format(
                mention=mention
            )
        )

    def _assign_assignee(self, conversation, assignee_id):
        """
        @param conversation - Intercom Conversation class object
        """
        LOGGER.debug("Assigning assignee {a_id} for conversation {c_id}".format(
            a_id=assignee_id,
            c_id=conversation.id
        ))

        user = Admin.find(id=assignee_id)
        mention = MENTION_TEMPLATE.format(
            intercom_app_id=Intercom.app_id,
            user_id=user.id,
            username=user.name
        )
        conversation.reply(
            type='admin', id=SUGGESTOR_ID,
            message_type='note', body="Autoassigned to {mention}".format(
                mention=mention
            )
        )
        conversation.assign(assignee_id=assignee_id, admin_id=assignee_id)

WebhookRoute = (r"/webhook/?(?P<action>[a-zA-Z]+)?", WebhookHandler)
