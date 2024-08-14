from openai import OpenAI
from app.utils.standard_response import StandardResponse
from app.utils.llm_utils import MathResponse
from app.core.config import settings

client = OpenAI()

def generate_text(client, user_input: str):
    try:
        completion = client.beta.chat.completions.parse(
            model=settings.LLM_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful math tutor."},
                {"role": "user", "content": user_input},
            ],
            response_format=MathResponse,
        )

        message = completion.choices[0].message.parsed

        return StandardResponse(
            status=settings.STATUS_SUCCESS,
            data=message.model_dump_json(),
            message=settings.SUCCESS
        )
    
    except Exception as err:
        return StandardResponse(
            status=settings.STATUS_ERROR,
            data=settings.STATUS_NULL,
            message=settings.FAIL
        )