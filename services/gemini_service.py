import google.generativeai as genai
from config.config import GEMINI_API_KEY, GEMINI_MODEL
import logging

logger = logging.getLogger(__name__)

def configure():
    genai.configure(api_key=GEMINI_API_KEY)

def ask_gemini(prompt, max_output_tokens=512, temperature=0.2):
    """
    Send a simple prompt to Gemini and return text reply.
    Keep server-side only; do not expose API key to clients.
    generation_config = genai.types.GenerationConfig( max_output_tokens=500,  # Adjust this number as needed
temperature=0.7         # Adjust this number as needed
)
    """
    # 1. Create the configuration object (Must do this first!)
    config = genai.types.GenerationConfig(
        max_output_tokens=max_output_tokens,
        temperature=temperature
    )

    try:
        configure()
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # 2. Pass the config object here (Notice the change!)
        response = model.generate_content(prompt)
        
        # ... rest of your code ...
        # response.text is common property; fallback if missing.
        text = getattr(response, "text", None) or (response.candidates[0].content if getattr(response, "candidates", None) else "")
        return text
    except Exception as e:
        logger.exception("Gemini request failed")
        return None
