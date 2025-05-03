import openai
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class TalkingPointsGenerator:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')

    async def generate_talking_points(
        self,
        meeting_title: str,
        meeting_description: str,
        participants: List[Dict[str, Any]],
        company_info: Dict[str, Any]
    ) -> List[str]:
        """
        Generate relevant talking points based on meeting context and participant information
        """
        # Prepare the prompt
        prompt = self._prepare_prompt(
            meeting_title,
            meeting_description,
            participants,
            company_info
        )

        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional meeting assistant that helps generate relevant talking points for meetings."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )

            # Extract and format talking points
            talking_points = self._process_response(response.choices[0].message.content)
            return talking_points

        except Exception as e:
            print(f"Error generating talking points: {str(e)}")
            return []

    def _prepare_prompt(
        self,
        meeting_title: str,
        meeting_description: str,
        participants: List[Dict[str, Any]],
        company_info: Dict[str, Any]
    ) -> str:
        """
        Prepare the prompt for the AI model
        """
        prompt = f"""Generate relevant talking points for the following meeting:

Meeting Title: {meeting_title}
Meeting Description: {meeting_description}

Participants:
"""
        
        for participant in participants:
            prompt += f"\n- {participant['name']}"
            if participant.get('headline'):
                prompt += f" ({participant['headline']})"
            if participant.get('company'):
                prompt += f" at {participant['company']}"

        if company_info:
            prompt += f"\n\nCompany Information:\n"
            prompt += f"Name: {company_info.get('name', '')}\n"
            prompt += f"Industry: {company_info.get('industry', '')}\n"
            prompt += f"Description: {company_info.get('description', '')}\n"

        prompt += "\n\nPlease generate 5-7 relevant talking points that would be valuable for this meeting. Focus on areas of common interest, potential collaboration opportunities, and relevant industry trends."

        return prompt

    def _process_response(self, response: str) -> List[str]:
        """
        Process the AI response into a list of talking points
        """
        # Split the response into lines and clean up
        points = [point.strip() for point in response.split('\n') if point.strip()]
        
        # Remove any numbering or bullet points
        points = [point.lstrip('123456789.-* ') for point in points]
        
        # Filter out any non-talking point lines
        points = [point for point in points if len(point) > 10 and not point.startswith(('Meeting', 'Participants', 'Company'))]
        
        return points[:7]  # Limit to 7 points maximum 