# -*- encoding: utf-8 -*-

import json
import enum
import abc

class JsonEnabled(abc.ABC):
    pass

class JsonEncoderIfJsonEnable(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, JsonEnabled):
            return o.__dict__
        elif isinstance(o, enum.Enum):
            return o.value
        else:
            return None