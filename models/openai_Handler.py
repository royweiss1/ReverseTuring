from llm import LLMHandler, MAX_TOKENS
from openai import OpenAI

# Example of a model-specific class
class OpenAIGPTHandler(LLMHandler):
    """Handler for OpenAI GPT models."""

    def __init__(self, role: str, test_mode: bool, api_key: str):
        super().__init__(role)
        self.client = OpenAI(api_key=api_key)
        if test_mode:
            self.model_name = "gpt-4o-mini" # this is the cheap model - use for testing...
        else:
            self.model_name = "gpt-4o"
        
        self.history = [{"role": "system", "content": self.system_prompt}]


    def send_message_interrogator(self, user_message: str, state: str) -> str:
        """
        Sends a message to the OpenAI GPT model and returns the response.

        Args:
            user_message (str): The user's message.
        Returns:
            str: The response from the Gemini model.
        """
        super().send_message_interrogator(user_message, state)
        
        try:
            response = self.client.chat.completions.create(
                messages=self.history,
                model=self.model_name,
                max_tokens=MAX_TOKENS
            )
            response = response.choices[0].message.content
        except Exception as e:
            response = f"[Error: {e}]"

        self.history.append({"role": "assistant", "content": response})
        return response
    

    def send_message_interrogated(self, user_message: str) -> str:
        """
        Sends a message to the OpenAI GPT model and returns the response.

        Args:
            user_message (str): The user's message.
        Returns:
            str: The response from the Gemini model.
        """
        super().send_message_interrogated(user_message)

        try:
            response = self.client.chat.completions.create(
                messages=self.history,
                model=self.model_name,
                max_tokens=MAX_TOKENS
            )
            response = response.choices[0].message.content
        except Exception as e:
            response = f"[Error: {e}]"

        self.history.append({"role": "assistant", "content": response})
        return response