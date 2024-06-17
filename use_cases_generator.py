import os

import openai
from dotenv import load_dotenv
from openai import OpenAI

from thread_helper import Helper
from tools import load, Model

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_use_case(prompt, assistant, thread, model=Model.GPT_4O.value):
    output_format = load('documents/usecase_generator_instructions.txt')
    use_case_examples_path = 'documents/usecase_generator_examples.txt'

    question = f"""
        Gere um caso de uso para: {prompt}. 
        Para isso, busque nos arquivos associados a você o conteúdo # Exemplos de Caso de Uso
        (no arquivo {use_case_examples_path})
    
        Adote o formato de saída abaixo.
    
        {output_format}
        """

    thread_helper = Helper(client)
    return thread_helper.include_message_and_process_response(question, thread, assistant, model)


def generate_use_case_old(user_prompt, model=Model.GPT_3_5):
    output_format = load('documents/usecase_generator_instructions.txt')

    system_prompt = f'''
        Você é um especialista em desenvolver casos de uso. Você deve adotar o padrão abaixo
        para gerar seu caso de uso:
        
        {output_format}
        
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
