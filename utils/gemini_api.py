import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
genai.configure(api_key=GENAI_API_KEY)

def get_player_analysis(player, ground):
    """ Get analysis of player from Gemini API """
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"Provide cricket stats for {player}, overall and on {ground}."
    response = model.generate_content(prompt)
    return response.text
