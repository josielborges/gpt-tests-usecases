import os

from dotenv import load_dotenv
from openai import OpenAI

from tools import Model

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def create_test_users(test_scenario, document, dictionary, model=Model.GPT_4O.value):
    system_prompt = f"""
    Você deve gerar um conjunto de dados de teste em formato JSON que serão utilizados com Selenium e Python para 
    simular e aprovar a navegabilidade de uma aplicação.
    
    Consulte os arquivos {dictionary[document + ".js"]}, {dictionary[document + ".html"]}, e 
    {dictionary[document + ".css"]} 
    para verificar os dados corretos de autenticação. 
    
    Gere quatro casos distintos de teste, com apenas um deles resultando em 'Aprovado'.
    Lembre-se de que os dados gerados devem ser em formato JSON válido.
    
    Inclua explicitamente na sua resposta o formato JSON esperado para os casos de teste.
    """

    response = client.chat.completions.create(
        model=model,
        response_format={
            'type': 'json_object'
        },
        messages=[
            {
                'role': 'system',
                'content': 'Você é um assistente útil projetado para gerar saídas em formato JSON. ' + system_prompt
            },
            {
                'role': 'user',
                'content': test_scenario
            }
        ]
    )

    return response.choices[0].message.content
