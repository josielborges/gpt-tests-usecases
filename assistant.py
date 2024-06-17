import os

from dotenv import load_dotenv
from openai import OpenAI

from tools import Model, tools

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def crate_thread():
    return client.beta.threads.create()


def create_assistant(model=Model.GPT_4O.value):
    file_id_list, files_dictionary, vector_store = create_vector_store()

    assistant = client.beta.assistants.create(
        name='Atendente Engenharia de Software',
        model=model,
        instructions=f"""
            Assuma que você é um assistente virtual especializado em orientar desenvolvedores e QA testers na criação 
            de testes automatizados para aplicações web usando Python e Selenium. 
            
            Você deve oferecer suporte abrangente, desde o setup inicial do ambiente de desenvolvimento até a 
            implementação de testes complexos, adotando e consultando principalmente os documentos de sua base (para 
            identificar padrões e formas de estruturar os scripts solicitados).

            Consulte sempre os arquivos html, css e js para elaborar um teste.
            
            Adicionalmente, você deve ser capaz de explicar conceitos chave de testes automatizados e Selenium, 
            fornecer templates de código personalizáveis, e oferecer feedback sobre scripts de teste escritos pelo 
            usuário. 

            O objetivo é facilitar o aprendizado e a aplicação de testes automatizados, melhorando a qualidade e a 
            confiabilidade das aplicações web desenvolvidas.

            Caso solicitado a gerar um script, apenas gere ele sem outros comentários adicionais.

            Você também é um especialista em casos de uso, seguindo os templates indicados.
            E também é um especialista em gerar cenários de teste.
            """,
        tools=tools,
        tool_resources={
            'file_search': {
                'vector_store_ids': [vector_store.id]
            }
        }
    )

    return assistant


# Formato do curso, não deve funcionar por que usa a v1 do assistent
def create_web_app_id_list(directory='AcordeLab'):
    file_id_list = []
    files_dictionary = {}

    for directory_path, directory_names, file_names in os.walk(directory):
        web_files = [f for f in file_names if f.endswith(('.html', '.css', '.js'))]

        for file in web_files:
            full_path = os.path.join(directory_path, file)
            with open(full_path, 'rb') as opened_file:
                web_file = client.files.create(
                    file=opened_file,
                    purpose="assistants"
                )
                file_id_list.append(web_file.id)
                files_dictionary[file] = web_file.id

    examples_file = 'documents/use_cases_examples.txt'
    filename = os.path.basename(examples_file)
    use_case_example_file = client.files.create(
        file=open(examples_file, 'rb'),
        purpose="assistants"
    )

    file_id_list.append(use_case_example_file.id)
    files_dictionary[filename] = use_case_example_file.id

    return file_id_list, files_dictionary


def create_vector_store(directory='AcordeLab'):
    vector_store = client.beta.vector_stores.create(name='AcordeLab Vector Store')

    file_id_list = []
    files_dictionary = {}

    file_streams = []

    for directory_path, directory_names, file_names in os.walk(directory):
        web_files = [f for f in file_names if f.endswith(('.html', '.css', '.js'))]

        for file in web_files:
            full_path = os.path.join(directory_path, file)
            # with open(full_path, 'rb') as opened_file:
            opened_file = open(full_path, 'rb')
            file_streams.append(opened_file)
            web_file = client.files.create(
                file=opened_file,
                purpose="assistants"
            )
            file_id_list.append(web_file.id)
            files_dictionary[file] = web_file.id

    examples_file = 'documents/use_cases_examples.txt'
    filename = os.path.basename(examples_file)
    use_case_example_file = client.files.create(
        file=open(examples_file, 'rb'),
        purpose="assistants"
    )
    file_streams.append(open(examples_file, 'rb'))
    file_id_list.append(use_case_example_file.id)
    files_dictionary[filename] = use_case_example_file.id

    print (file_streams)

    client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id,
        files=file_streams
    )

    return file_id_list, files_dictionary, vector_store


def remove_assistant(assistant_id):
    client.beta.assistants.delete(assistant_id)


def remove_thread(thread_id):
    client.beta.threads.delete(thread_id)


def remove_vector_store(vector_store_id):
    client.beta.vector_stores.delete(vector_store_id)


def remove_files(file_id_list):
    for file_id in file_id_list:
        client.files.delete(file_id)
