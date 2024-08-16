import json
from openai import OpenAI
from fastapi import status
from app.utils.standard_response import StandardResponse
from app.utils.llm_utils import MathResponse
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_text(user_input: str):
    try:
        completion = client.beta.chat.completions.parse(
            model=settings.LLM_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful math tutor."},
                {"role": "user", "content": user_input},
            ],
            response_format=MathResponse,
        )

        message = completion.choices[0].message.parsed.model_dump_json()

        return StandardResponse(
            status=settings.STATUS_SUCCESS,
            status_code=status.HTTP_200_OK,
            data=json.loads(message),
            message=settings.SUCCESS
        ).to_json_response()
    
    except Exception as err:
        return StandardResponse(
            status=settings.STATUS_ERROR,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data=settings.STATUS_NULL,
            message=settings.ERROR
        ).to_json_response()