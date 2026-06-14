import json
import os

from openai import OpenAI

from app.services.openai_service import (
    OpenAIService
)
client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

class AIProfileGenerator:

    @staticmethod
    def generate(
        chart_json,
        profile_json
    ):

        system_prompt = """
You are an expert Vedic astrologer, behavioral psychologist,
executive coach and human potential analyst.

Generate a premium Cosmic Alignment Profile.

Write in a style similar to a personalized life strategy report.

Avoid astrology jargon.

Focus on:

- personality
- emotional tendencies
- strengths
- blind spots
- growth opportunities
- practical life guidance

The reader should feel deeply understood.

Never use fear-based predictions.

Never mention houses, planetary degrees,
nakshatra names or technical astrology terms.

Return valid JSON only.
"""

        user_prompt = f"""
Chart:

{json.dumps(chart_json, indent=2)}

Structured Profile:

{json.dumps(profile_json, indent=2)}

Return:

{{
  "executive_summary":"",

  "core_personality":"",

  "emotional_patterns":"",

  "strengths_narrative":"",

  "blind_spots":"",

  "growth_path":"",

  "alignment_advice":"",

 "natural_potential_index":0,
    
  "core_gifts":[],

  "growth_edges":[],

  "untapped_potential":[],

  "energy_drains":[],

  "recommended_focus":[]
}}
"""

        response = OpenAIService.chat(
            system_prompt,
            user_prompt
        )
        print("\n===== AI RESPONSE =====")
        print(response)
        print("=======================\n")
        return json.loads(response)