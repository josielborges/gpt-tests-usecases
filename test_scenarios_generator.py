import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = 'gpt-3.5-turbo'


def generate_test_scenario(usecase):
    system_prompt = f'''
        Você é um especialista em desenvolver cenários de teste para validar uma aplicação web, quanto sua navegação.
        Para isso, considere o caso de uso destacado em: {usecase}.
        
        Seu cenário de teste deve fornecer dados suficientes para validar uma aplicação HTML, CSS e JS e para que
        possa ser implementado usando Python e Selenium.
    '''

    response = client.chat.completions.create(
        model=model,
        temperature=0.5,
        messages=[
            {
                'role': 'system',
                'content': system_prompt,
            }
        ]
    )

    return response.choices[0].message.content
