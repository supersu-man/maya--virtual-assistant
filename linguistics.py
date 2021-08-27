from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_EN

import io
import json

with io.open("dataset.json") as f:
    dataset = json.load(f)

seed = 50
engine = SnipsNLUEngine(config=CONFIG_EN, random_state=seed)
engine.fit(dataset)


def getIntent(command):
    parsing = engine.parse(command)
    intentName = parsing['intent']['intentName']
    value=''
    if len(parsing['slots'])>0:
        value = parsing['slots'][0]['rawValue']
    return intentName, value
