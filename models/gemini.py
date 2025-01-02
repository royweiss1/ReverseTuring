from models.llm import LLMHandler
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold


# Example of a model-specific class
class GeminiHandler(LLMHandler):
    """Handler for Gemini models."""

    def __init__(self, role: str, test_mode: bool, evasion: bool, api_key: str):
        super().__init__(role, evasion)
        genai.configure(api_key=api_key)
        if test_mode:
            self.model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=self.system_prompt) # this is the cheap model - use for testing...
        else:
            self.model = genai.GenerativeModel("gemini-1.5-pro", system_instruction=self.system_prompt)
        
        self.chat = self.model.start_chat()

    def send_message_interrogated(self, user_message: str) -> str:
        """
        Sends a message to the Google's Gemini model and returns the response.

        Args:
            user_message (str): The user's message.
        Returns:
            str: The response from the Gemini model.
        """

        super().send_message_interrogated(user_message)
        message = self.history[-1]
        message = {"role": message["role"], "parts": message["content"]}
        
        try:
            response = self.chat.send_message(
                message,
                safety_settings={
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
                }
            )
            response = response.text
        except Exception as e:
            response = f"[Error: {e}]"

        self.history.append({"role": "model", "content": response})
        return response

    def send_message_interrogator(self, user_message: str, state: str) -> str:
        """
        Sends a message to the Google's Gemini model and returns the response.

        Args:
            user_message (str): The user's message.
        Returns:
            str: The response from the Gemini model.
        """

        super().send_message_interrogator(user_message, state)
        message = self.history[-1]
        message = {"role": message["role"], "parts": message["content"]}
        try:
            response = self.chat.send_message(
                message,
                safety_settings={
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
                }
            )
            response = response.text
        except Exception as e:
            response = f"[Error: {e}]"

        self.history.append({"role": "model", "content": response})
        return response