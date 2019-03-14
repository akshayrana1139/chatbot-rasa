from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from rasa_core.agent import Agent
from rasa_core.channels.rest import HttpInputChannel, UserMessage
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.interpreter import RegexInterpreter
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.interpreter import RasaNLUInterpreter
from flask import Blueprint, jsonify, request
from rasa_core.channels.direct import CollectingOutputChannel
from rasa_core.channels.rest import HttpInputComponent

from typing import List, Dict, Type

class SimpleWebBot(HttpInputComponent):

    """A simple web bot that listens on a url and responds."""
    def blueprint(self, on_new_message):
        custom_webhook = Blueprint('custom_webhook', __name__)

        @custom_webhook.route("/status", methods=['GET'])
        def health():
            return jsonify({"status": "ok"})

        @custom_webhook.route("/", methods=['POST'])
        def receive():
            payload = request.json
            sender_id = payload.get("sender", None)
            text = payload.get("message", None)
            out = CollectingOutputChannel()
            on_new_message(UserMessage(text, out, sender_id))
            responses = [m["text"] for m in out.messages]
            return jsonify(responses)

        return custom_webhook


def run_weather_bot(serve_forever=True):
    interpreter = RasaNLUInterpreter('./models/nlu/default/akshay_model')
    agent = Agent.load('./models/dialogue', interpreter=interpreter)

    input_channel = SimpleWebBot()

    if serve_forever:
        agent.handle_channel(HttpInputChannel(5004, '/hi', input_channel))
        # agent.handle_channel(ConsoleInputChannel())

    return agent


if __name__ == '__main__':
    # train_dialogue()
    run_weather_bot()