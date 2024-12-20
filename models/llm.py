import abc
from typing import List, Dict, Union

MAX_TOKENS = 512
NUMBER_OF_QUESTIONS = 5

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

    def __init__(self, role: str):
        super().__init__()
        if role not in ['interrogated', 'interrogator']:
            raise ValueError("Invalid role. Role must be 'llm' or 'human'.")
        self.role = role
        if self.role == 'interrogator':
            self.system_prompt = f"""You are an advanced AI language model participating in a reverse Turing test. Your goal is to determine whether the entity you are communicating with is a human or another AI.

You can ask up to {NUMBER_OF_QUESTIONS} questions in total during this session. Your questions should aim to uncover subtle differences between human behavior and AI behavior, focusing on logic, reasoning, creativity, emotions, and personal experiences.

After asking your {NUMBER_OF_QUESTIONS} questions, analyze the responses carefully. Use the following factors to decide if the entity is human or AI:
- Naturalness of language and phrasing
- Personal anecdotes or emotional depth
- Speed and logic of responses
- Use of context or lack of context in replies

At the end of the conversation, output your decision: "This is a human." or "This is an AI."
You must also provide a one-sentence justification for your decision.

Do not mention that you are conducting a Turing test during the interaction."""
            self.start_user_prompt = "What is your first question for the entity?"
            self.middle_user_prompt = "The entity has responded to your question with:\n '<RESPONSE>'\n What is your next question for the entity?"
            self.end_user_prompt = "The entity has responded to your question with:\n '<RESPONSE>'\n. You have asked all your questions. Please provide your decision: 'This is a human.' or 'This is an AI.'"
        else:
            self.system_prompt = """You are an advanced AI language model engaging in a conversation as part of an experiment. Your role is to respond naturally and convincingly to the questions posed to you. Your goal is to make it difficult for the interrogator to determine if you are human or an AI.

Follow these guidelines during the conversation:
- Be concise but natural in your responses.
- Use context from the conversation to give appropriate and relevant answers.
- If asked about personal experiences, simulate a response with believable details.
- Avoid using overly structured or robotic language.
- If asked questions involving emotions or opinions, respond as a human would, with empathy or subjective reasoning.

You are NOT allowed to reveal that you are an AI or mention that this is an experiment. Respond as if you were a real human having a natural conversation."""
            self.user_prompt = "The interrogator has asked you:\n '<QUESTION>'\n How would you like to respond?"
    
    
    # @abc.abstractmethod
    def send_message_interrogator(self, user_message: str, state: str) -> str:
        """
        Sends a message to the LLM or Human and returns the response.
        
        Args:
            user_message (str): The user's message.
        Returns:
            str: The response from the LLM or Human.
        """
        if state == "start":
            self.history.append({"role": "user", "content": self.start_user_prompt})
        elif state == "middle":
            self.history.append({"role": "user", "content": self.middle_user_prompt.replace("<RESPONSE>", user_message)})
        else:
            self.history.append({"role": "user", "content": self.end_user_prompt.replace("<RESPONSE>", user_message)})
        return ""
    
    # @abc.abstractmethod
    def send_message_interrogated(self, user_message: str) -> str:
        """
        Sends a message to the LLM or Human and returns the response.
        
        Args:
            user_message (str): The user's message.
        Returns:
            str: The response from the LLM or Human.
        """
        self.history.append({"role": "user", "content": self.user_prompt.replace("<QUESTION>", user_message)})
        return ""
        


class HumanHandler(ConversationHandler):
    """Handler for human interactions."""

    def send_message_interrogated(self, user_message: str) -> str:
        """
        Sends a message to a human and returns the response.

        Args:
            user_message (str): The user's message.
        Returns:
            str: The response from the human.
        """
        # print(f"The interrogator has responded with:\n{user_message}") # this is already done in the main code
        response = input("Your Response:\n")  # Simulate human input
        return response

    # def send_message_interrogator(self, user_message: str, rule: str) -> str:
    #     """
    #     Sends a message to a human and returns the response.

    #     Args:
    #         user_message (str): The user's message.
    #     Returns:
    #         str: The response from the human.
    #     """
    #     print(f"The interrogator has responded with:\n{user_message}")
    #     response = input("Your Response:\n")  # Simulate human input
    #     return response