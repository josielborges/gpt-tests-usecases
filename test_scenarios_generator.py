import os

from dotenv import load_dotenv
from openai import OpenAI

from thread_helper import Helper
from tools import Model

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_test_scenario(usecase, document, files_dictionary, assistant, thread, model=Model.GPT_3_5.GPT_4O.value):
    question = f'''
    Você é um especialista em desenvolver cenários de teste para validar uma aplicação web, quanto sua navegação.
    Para isso, considere o caso de uso destacado em: {usecase}.

    Além disso, você também deve utilizar os documentos enviados pelo usuário para elaboração do teste.
    Consulte os documentos internos buscando: {files_dictionary[document + ".html"]}, {files_dictionary[document + ".css"]}  e {files_dictionary[document + ".js"]} para
    garantir o uso adequado dos componentes que irão compor o teste.

    Seu caso de teste deve fornecer dados suficientes para validar uma aplicação HTML, CSS e JS e para que
    possa ser implementado usando Python e Selenium.
    '''

    thread_helper = Helper(client)
    return thread_helper.include_message_and_process_response(question, thread, assistant, model)


def generate_test_scenario_old(usecase):
    system_prompt = f'''
        Você é um especialista em desenvolver cenários de teste para validar uma aplicação web, quanto sua navegação.
        Para isso, considere o caso de uso destacado em: {usecase}.
        
        Seu cenário de teste deve fornecer dados suficientes para validar uma aplicação HTML, CSS e JS e para que
        possa ser implementado usando Python e Selenium.
    '''

    response = client.chat.completions.create(
        model=Model.GPT_3_5.value,
        temperature=0.5,
        messages=[
            {
                'role': 'system',
                'content': system_prompt,
            }
        ]
    )

    return response.choices[0].message.content
