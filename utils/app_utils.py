from flask import Blueprint, g

global_util_app = Blueprint('global_util_app', __name__)

def inject_globals():
    return {
        'alert': getattr(g, 'alert', None)
    }

def set_alert(alert_type: str, strong_message: str, message: str) -> None:
    g.alert = {
        "type": alert_type,
        "strong_message": strong_message,
        "message": message
    }
