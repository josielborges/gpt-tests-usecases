import os

import openai
from dotenv import load_dotenv
from openai import OpenAI

from tools import load

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = 'gpt-3.5-turbo'
fine_tuned_model = os.getenv("FINE_TUNED_MODEL")


def generate_use_case():
    instructions = load('documents/usecase_generator_instructions.txt')

    system_prompt = f'''
        Você é um especialista em desenvolver casos de uso. Você deve adotar o padrão abaixo
        para gerar seu caso de uso:
        
        {instructions}
        
        Considere os dados de entrada sugeridos pelo usuário.
    '''

    user_prompt = """"
        Ana que deseja realizar login na plataforma AcordeLab.
    """

    response = openai.chat.completions.create(
        model=fine_tuned_model,
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
