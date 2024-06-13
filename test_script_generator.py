import os

import openai
from dotenv import load_dotenv
from openai import OpenAI

from tools import load

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = 'gpt-3.5-turbo'


def generate_script(usecase, test_scenario):
    company_document = load('documents/acord_lab.txt')

    system_prompt = f'''
        Você é um especialista em gerar scripts de teste para elaboração de casos de uso e cenários de teste.
        Considere o contexto da empresa disponível em : {company_document}
    
        Seu cenário de teste deve fornecer um script em Selenium e deve Utilizar o chromium como driver para isso
        Além disso, seu código deve ser escrito em Python e deve utilizar apenas as bibliotecas em destaque.
        Dando uma pausar de 3 segundos antes de fechar o script.
        Não use headless.
        
        # Bibliotecas
        
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        import time
    '''

    user_prompt = f'''
        Considere o caso de uso {usecase} e o cenário de teste {test_scenario}.
    
        Crie um script para gerar um teste automatizado para ambos.
    '''

    response = openai.chat.completions.create(
        model=model,
        temperature=0.5,
        messages=[
            {
                'role': 'system',
                'content': system_prompt
            },
            {
                'role': 'user',
                'content': user_prompt
            }
        ]
    )

    return response.choices[0].message.content
