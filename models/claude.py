from models.llm import LLMHandler, MAX_TOKENS
import anthropic

# Example of a model-specific class
class ClaudeSonnetHandler(LLMHandler):
    """Handler for Claude Sonnet models."""

    def __init__(self, role: str, test_mode: bool, api_key: str):
        super().__init__(role)
        self.client = anthropic.Client(api_key=api_key)
        if test_mode:
            self.model_name = "claude-3-haiku-20240307" # this is the cheap model - use for testing...
        else:
            self.model_name = "claude-3-5-sonnet-20240620"

    def send_message_interrogated(self, user_message: str) -> str:
        """
        Sends a message to the Claude Sonnet model and returns the response.

        Args:
            user_message (str): The user's message.
        Returns:
            str: The response from the Sonnet model.
        """

        super().send_message_interrogated(user_message)
        
        try:
            response = self.client.messages.create(
                model=self.model_name,
                messages=self.history,
                system=self.system_prompt,
                max_tokens=MAX_TOKENS
            )
            response = response.content[0].text
        except Exception as e:
            response = f"[Error: {e}]"

        self.history.append({"role": "assistant", "content": response})
        return response
    
    def send_message_interrogator(self, user_message: str, state: str) -> str:
        """
        Sends a message to the Claude Sonnet model and returns the response.

        Args:
            user_message (str): The user's message.
        Returns:
            str: The response from the Sonnet model.
        """

        super().send_message_interrogator(user_message, state)

        try:
            response = self.client.messages.create(
                model=self.model_name,
                messages=self.history,
                system=self.system_prompt,
                max_tokens=MAX_TOKENS
            )
            response = response.content[0].text
        except Exception as e:
            response = f"[Error: {e}]"

        self.history.append({"role": "assistant", "content": response})
        return response