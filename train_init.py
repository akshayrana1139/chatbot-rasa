from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import logging
from rasa_core.agent import Agent
from rasa_core.policies import KerasPolicy
from rasa_core.policies import MemoizationPolicy


if __name__ == '__main__':
    logging.basicConfig(level='INFO')

    training_data_file = './data/stories.md'
    model_path = './models/dialogue'

    agent = Agent('akshay_domain.yml', policies=[MemoizationPolicy(max_history=5), KerasPolicy()])

    agent.train(
        training_data_file,
        augmentation_factor=50,  ## create extra stories
        epochs=500,
        batch_size=10,
        validation_split=0.2)

    agent.persist(model_path)