import os

from dotenv import load_dotenv
from openai import OpenAI
import json

from tools import Model

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_embedding(text, model=Model.EMBEDDING.value):
    return client.embeddings.create(
        input=text,
        model=model
    ).data[0].embedding


def retrieve_documents(metadata_path):
    string_json = open(metadata_path)
    metadata_json = json.load(string_json)

    descriptions = []
    metadata = []

    for object in metadata_json:
        descriptions.append(object['meta_description'])
        metadata.append(object)

    return descriptions, metadata


def process_documents(directory='AcordeLab'):
    print('Processing documents...')

    allowed_extensions = ('.html', '.cee', '.js')
    metadata = []
    descriptions = []

    for dir_path, dir_names, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(allowed_extensions):
                file_path = os.path.join(dir_path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_text = file.read()
                meta_description = generate_embedding(file_text, filename)
                metadata.append({
                    'document': filename,
                    'meta_description': meta_description,
                    'file_path': file_path
                })
                descriptions.append(meta_description)

    return descriptions, metadata


def generate_meta_data(document, file_name, model=Model.GPT_4O.value):
    system_prompt = f'''
        Analise o documento fornecido e gere um resumo conciso do seu conteúdo. 
        O documento pode ser uma página web com HTML, CSS, e JavaScript, detalhando 
        aspectos como design, funcionalidades interativas e informações específicas,
        ou um arquivo de texto com orientações e exemplos. O resumo deve capturar 
        os elementos centrais e o propósito do documento, destacando 
        características chave e tecnologias utilizadas. Este resumo será usado 
        para criar um embedding, otimizando a recuperação do documento em um 
        banco de dados vetorial.

        Sua meta-descrição deve incluir:

        - Nome do Arquivo: {file_name}
        - Propósito do Arquivo: Enfatize a ação principal do usuário do arquivo de acordo com o conteúdo. Não mencione outros tipos de linguagem a não ser a utilizada para escrever o documento. Disponível no arquivo {nome_arquivo}.
        - Tipo de Arquivo: HTML, CSS ou JS (escolha com base na linguagem usada)

        Como saída gere apenas a meta-descrição que será utilizada para gerar embeddings.
    '''

    user_prompt = f'Gere uma meta-descrição para o documento: {document}'

    response = client.chat.completions.create(
        model=model,
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

# print(generate_embedding('Olá, mundo!'))
