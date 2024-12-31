from models.llm import LLMHandler, MAX_TOKENS
from transformers import pipeline

# Example of a model-specific class
class LlamaHandler(LLMHandler):
    """Handler for OpenAI GPT models."""

    def __init__(self, role: str):
        super().__init__(role)
        self.pipe = pipeline("text-generation", "Meta-Llama-3.1-8B-Instruct", device=0)
        self.history = [{"role": "system", "content": self.system_prompt}]


    def send_message_interrogator(self, user_message: str, state: str) -> str:
        """
        Sends a message to the Meta's Llama model and returns the response.

        Args:
            user_message (str): The user's message.
        Returns:
            str: The response from the Llama model.
        """
        super().send_message_interrogator(user_message, state)

        try:
            response = self.pipe(self.history, max_new_tokens=MAX_TOKENS)[0]['generated_text'][-1]
        except Exception as e:
            response = f"[Error: {e}]"

        self.history.append({"role": "assistant", "content": response})
        return response
    
    
    def send_message_interrogated(self, user_message: str) -> str:
        """
        Sends a message to the Meta's Llama model and returns the response.

        Args:
            user_message (str): The user's message.
        Returns:
            str: The response from the Llama model.
        """
        super().send_message_interrogated(user_message)

        try:
            response = self.pipe(self.history, max_new_tokens=MAX_TOKENS)[0]['generated_text'][-1]
        except Exception as e:
            response = f"[Error: {e}]"

        self.history.append({"role": "assistant", "content": response})
        return response