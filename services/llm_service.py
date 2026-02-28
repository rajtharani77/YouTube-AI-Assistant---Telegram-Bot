"""
LLM Service
Handles interaction with AI providers (Google Gemini / future OpenAI support)
"""

import google.generativeai as genai
from config.settings import Config
from utils.logger import logger
from utils.exceptions import ModelError, ConfigurationError

class LLMService:
    """LLM Provider Manager"""

    def __init__(self):
        self.model = self._initialize_model()

    def _initialize_model(self):
        """Initialize configured LLM provider"""

        try:
            provider = Config.LLM_PROVIDER.lower()

            if provider == "google":

                if not Config.GOOGLE_API_KEY:
                    raise ConfigurationError(
                        "GOOGLE_API_KEY missing in environment"
                    )

                genai.configure(api_key=Config.GOOGLE_API_KEY)

                logger.info(
                    f"✅ Gemini initialized | Model: {Config.MODEL_NAME}"
                )

                return genai.GenerativeModel(
                    model_name=Config.MODEL_NAME
                )

            else:
                raise ConfigurationError(
                    f"Unsupported LLM provider: {provider}"
                )

        except Exception as e:
            logger.error(f"LLM initialization failed: {e}")
            raise ConfigurationError(str(e))

    def ask(
        self,
        prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 2048,
    ) -> str:
        """
        Send prompt to LLM
        """
        try:
            if not prompt or not isinstance(prompt, str):
                raise ValueError("Prompt must be a valid string")
            logger.info(" Sending request to LLM")
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": max(0.0, min(temperature, 1.0)),
                    "max_output_tokens": max_tokens,
                },
            )
            text = getattr(response, "text", None)
            if not text:
                raise ModelError("Model returned empty response")
            logger.info("✅ LLM response received")
            return text.strip()
        except Exception as e:
            logger.error(f"LLM request failed: {e}")
            raise ModelError(str(e))

llm_service = LLMService()

def ask_llm(prompt: str, **kwargs) -> str:
    """
    Public helper function used across project
    """
    return llm_service.ask(prompt, **kwargs)