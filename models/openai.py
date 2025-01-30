from models.llm import LLMHandler, MAX_TOKENS
import openai


class OpenAIGPTHandler(LLMHandler):
    """Handler for OpenAI GPT models."""

    def __init__(self, role: str, test_mode: bool, evasion: bool, api_key: str):
        super().__init__(role, evasion)
        openai.api_key = api_key  # Set the OpenAI API key
        self.model_name = "gpt-4o-mini" if test_mode else "gpt-4o"
        self.history = [{"role": "system", "content": self.system_prompt}]

    def send_message_interrogator(self, user_message: str, state: str) -> str:
        """
        Sends a message to the OpenAI GPT model and returns the response.

        Args:
            user_message (str): The user's message.
            state (str): Current state of the conversation.
        Returns:
            str: The response from the model.
        """
        super().send_message_interrogator(user_message, state)

        self.history.append({"role": "user", "content": user_message})

        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=self.history,
                max_tokens=MAX_TOKENS
            )
            response_text = response['choices'][0]['message']['content']
        except Exception as e:
            response_text = f"[Error: {e}]"

        self.history.append({"role": "assistant", "content": response_text})
        return response_text

    def send_message_interrogated(self, user_message: str) -> str:
        """
        Sends a message to the OpenAI GPT model and returns the response.

        Args:
            user_message (str): The user's message.
        Returns:
            str: The response from the model.
        """
        super().send_message_interrogated(user_message)

        self.history.append({"role": "user", "content": user_message})

        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=self.history,
                max_tokens=MAX_TOKENS
            )
            response_text = response['choices'][0]['message']['content']
        except Exception as e:
            response_text = f"[Error: {e}]"

        self.history.append({"role": "assistant", "content": response_text})
        return response_text
