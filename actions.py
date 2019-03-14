from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet

class ActionWeather(Action):
    def name(self):
        return 'action_weather' ## to be used in stories.md

    def run(self, dispatcher, tracker, domain):
        loc = tracker.get_slot('location')
        response = """Its v hot"""
        dispatcher.utter_message(response)
        return None


action = ActionWeather()
action.resets_topic()
print(type(action))




