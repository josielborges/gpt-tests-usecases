import os

import openai
from dotenv import load_dotenv
from openai import OpenAI

from thread_helper import Helper
from tools import load, Model

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_script(test_scenario, document, files_dictionary, assistant, thread, model=Model.GPT_3_5.GPT_4O.value):
    question = f'''
        Você é um especialista em gerar scripts de teste para elaboração de casos de uso e cenários de teste.

        Seu cenário de teste deve fornecer um script em Selenium e deve utilizar o chromium como driver para isso
        Além disso, seu código deve ser escrito em Python e deve utilizar apenas as bibliotecas em destaque.
        Dando uma pausar de 3 segundos antes de fechar o script.

        # Bibliotecas

        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        import time

        # Arquivos que farão parte do teste

        Consulte nos arquivos internos os documentos: {files_dictionary[document + ".html"]}, {files_dictionary[document + ".css"]}  e {files_dictionary[document + ".js"]}

        Além disso, considere o {test_scenario} para elaborar o teste em selenium.

        # Saída

        Apenas um script em python com comentários em português para auxiliar a pessoa desenvolvedora
    '''

    thread_helper = Helper(client)
    return thread_helper.include_message_and_process_response(question, thread, assistant, model)


def generate_script_old(usecase, test_scenario):
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
        model=Model.GPT_3_5.value,
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
