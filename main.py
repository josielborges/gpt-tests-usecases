import openai

from assistant import (create_assistant, create_vector_store, crate_thread, remove_vector_store, remove_files,
                       remove_assistant, remove_thread)
from test_scenarios_generator import generate_test_scenario
from test_script_generator import generate_script
from tools import save, Model
from use_cases_generator import generate_use_case


def main():
    # user_prompt = input('Digite um caso de uso: ')
    user_prompt = 'Ana deseja logar na plataforma'
    page = 'index'

    file_id_list, files_dictionary, vector_store = create_vector_store('AcordeLab')
    assistant = create_assistant(Model.GPT_4O.value)
    thread = crate_thread()

    try:
        print(f'thread id: {thread.id}')
        use_cases = generate_use_case(user_prompt, assistant, thread)
        print(f'\nCaso de uso:\n{use_cases}')

        test_scenario = generate_test_scenario(use_cases, page, files_dictionary, assistant, thread)
        print(f'\nCenarios de teste:\n{test_scenario}')

        script_test = generate_script(test_scenario, page, files_dictionary, assistant, thread)
        print(f'\nScript teste:\n{script_test}')

        save(f'generated_scripts/script_{page}.py', script_test)

    except Exception as e:
        print('Error: ', e)
    finally:
        print('Apagando arquivos gerados ...')
        remove_files(file_id_list)
        remove_vector_store(vector_store.id)
        remove_assistant(assistant.id)
        remove_thread(thread.id)

    # use_cases = generate_use_case(user_prompt, Model.GPT_3_5)
    # print(f'\nCaso de uso - Modelo padrão:\n{use_cases}')
    #
    # use_cases = generate_use_case(user_prompt, Model.GPT_FINE_TUNED)
    # print(f'\nCaso de uso - Modelo fine tuned:\n{use_cases}')

    # test_scenario = generate_test_scenario(use_cases)
    # print(f'\nCenarios de teste:\n{test_scenario}')
    #
    # script_test = generate_script(use_cases, test_scenario)
    # print(f'\nScript teste:\n{script_test}')

    # save('data/script_test.py', script_test)


if __name__ == '__main__':
    main()
