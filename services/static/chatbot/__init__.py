# chatbot/__init__.py

"""
Chatbot package initializer.

This file makes the `chatbot` directory a Python module and exposes
the main chatbot logic so it can be imported easily in app.py:

    from chatbot import get_bot_response
"""

from .logic import handle_message
__all__ = ["get_bot_response"]
