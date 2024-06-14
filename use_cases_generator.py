import os

import openai
from dotenv import load_dotenv
from openai import OpenAI

from tools import load, Model

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_use_case(user_prompt, model=Model.GPT_3_5):
    instructions = load('documents/usecase_generator_instructions.txt')

    system_prompt = f'''
        Você é um especialista em desenvolver casos de uso. Você deve adotar o padrão abaixo
        para gerar seu caso de uso:
        
        {instructions}
        
        Considere os dados de entrada sugeridos pelo usuário.
    '''

    response = openai.chat.completions.create(
        model=model.value,
        temperature=0.5,
        messages=[
            {
                'role': 'system',
                'content': system_prompt,
            },
            {
                'role': 'user',
                'content': user_prompt,
            }
        ]
    )

    return response.choices[0].message.content
