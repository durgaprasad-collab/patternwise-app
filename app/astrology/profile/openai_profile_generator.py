import openai
import json
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class OpenAIProfileGenerator:

    @staticmethod
    def generate(chart):

        prompt = f"""
Create a Cosmic Alignment Profile.

Chart Facts:

{json.dumps(chart, indent=2)}

Return JSON only.

Format:

{{
  "core_gifts": [],
  "growth_edges": [],
  "untapped_potential": [],
  "energy_drains": []
}}
"""

        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "system",
                    "content":
                    "You are an expert Vedic astrologer."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={
                "type": "json_object"
            }
        )

        return json.loads(
            response.choices[0].message.content
        )