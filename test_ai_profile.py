import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)   
print(os.getenv("OPENAI_API_KEY"))
from app.astrology.profile.ai_profile_generator import (
    AIProfileGenerator
)

chart = {
    "ascendant": {
        "sign": "Libra",
        "nakshatra": "Swati"
    },

    "planets": {
        "Moon": {
            "sign": "Leo",
            "nakshatra": "Purva Phalguni"
        }
    }
}

profile = {
    "core_gifts": [
        "Diplomacy",
        "Leadership"
    ]
}

result = AIProfileGenerator.generate(
    chart,
    profile
)

print(result)