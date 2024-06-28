from langchain_community.llms.openai import OpenAI
import os

async def get_llm_response(prompt: str):
    openai_api_key = os.getenv("OPENAI_API_KEY")
    llm = OpenAI(api_key=openai_api_key)
    response_text = await llm.agenerate([prompt])
    return response_text
