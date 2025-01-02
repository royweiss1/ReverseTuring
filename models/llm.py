import abc
from typing import List, Dict, Union
from models.prompts import (
    INTERROGATOR_SYSTEM_PROMPT,
    INTERROGATOR_START_USER_PROMPT,
    INTERROGATOR_MIDDLE_USER_PROMPT,
    INTERROGATOR_END_USER_PROMPT,
    INTERROGATED_SYSTEM_PROMPT,
    INTERROGATED_USER_PROMPT,
    INTERROGATED_EVASION_SYSTEM_PROMPT,
    INTERROGATED_EVASION_USER_PROMPT,
)

MAX_TOKENS = 512


class ConversationHandler(abc.ABC):
    """Abstract base class for handling conversations."""

    def __init__(self):
        self.history = []

    @abc.abstractmethod
    def send_message_interrogated(self, user_message: str) -> str:
        """
        Sends a message to the LLM or Human and returns the response.

        Args:
            user_message (str): The user's message.
        Returns:
            str: The response from the LLM or Human.
        """
        pass


class LLMHandler(ConversationHandler):
    """Generic handler for LLMs."""

    def __init__(self, role: str, evasion: bool):
        super().__init__()
        if role not in ['interrogated', 'interrogator']:
            raise ValueError("Invalid role. Role must be 'llm' or 'human'.")
        self.role = role
        if self.role == 'interrogator':
            self.system_prompt = INTERROGATOR_SYSTEM_PROMPT
            self.start_user_prompt = INTERROGATOR_START_USER_PROMPT
            self.middle_user_prompt = INTERROGATOR_MIDDLE_USER_PROMPT
            self.end_user_prompt = INTERROGATOR_END_USER_PROMPT
        elif self.role == 'interrogated' and evasion:
            self.system_prompt = INTERROGATED_EVASION_SYSTEM_PROMPT
            self.user_prompt = INTERROGATED_EVASION_USER_PROMPT
        else:
            self.system_prompt = INTERROGATED_SYSTEM_PROMPT
            self.user_prompt = INTERROGATED_USER_PROMPT

    def send_message_interrogator(self, user_message: str, state: str) -> str:
        if state == "start":
            self.history.append({"role": "user", "content": self.start_user_prompt})
        elif state == "middle":
            self.history.append(
                {"role": "user", "content": self.middle_user_prompt.replace("<RESPONSE>", user_message)})
        else:
            self.history.append({"role": "user", "content": self.end_user_prompt.replace("<RESPONSE>", user_message)})
        return ""

    def send_message_interrogated(self, user_message: str) -> str:
        self.history.append({"role": "user", "content": self.user_prompt.replace("<QUESTION>", user_message)})
        return ""


class HumanHandler(ConversationHandler):
    """Handler for human interactions."""

    def send_message_interrogated(self, user_message: str) -> str:
        response = input("Your Response:\n")  # Simulate human input
        return response
