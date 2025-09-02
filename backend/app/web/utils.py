# app/web/utils.py
import json
from datetime import date, datetime
import numpy as np
import math
from flask import current_app

# Note: All JSON helper functions from web_server.py have been moved here
# to break the circular import dependency.

def convert_numpy_types(obj):
    """Recursively converts NumPy types in dicts and lists to native Python types."""
    if isinstance(obj, dict):
        return {convert_numpy_types(key): convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        if np.isnan(obj) or np.isinf(obj):
            return None
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    elif isinstance(obj, (date, datetime)):
        return obj.isoformat()
    else:
        return obj

class NumpyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            from langchain_core.messages import BaseMessage
            if isinstance(obj, BaseMessage):
                return {"type": obj.__class__.__name__, "content": str(obj.content)}
        except ImportError:
            pass

        cleaned_obj = convert_numpy_types(obj)
        if cleaned_obj is not obj:
            return cleaned_obj

        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        
        try:
            return super().default(obj)
        except TypeError:
            return str(obj)

def convert_messages_to_dict(obj):
    """Recursively convert LangChain message objects to dictionaries."""
    try:
        from langchain_core.messages import BaseMessage
        is_message = isinstance(obj, BaseMessage)
    except ImportError:
        is_message = False

    if is_message:
        return {"type": obj.__class__.__name__, "content": str(obj.content)}
    elif isinstance(obj, dict):
        return {k: convert_messages_to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_messages_to_dict(elem) for elem in obj]
    else:
        return obj

def custom_jsonify(data):
    """
    Custom jsonify function that uses the NumpyJSONEncoder and the application context.
    It uses `current_app` to avoid direct dependency on the `app` object.
    """
    return current_app.response_class(
        json.dumps(convert_numpy_types(data), cls=NumpyJSONEncoder),
        mimetype='application/json'
    )
