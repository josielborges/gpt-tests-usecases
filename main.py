from test_scenarios_generator import generate_test_scenario
from test_script_generator import generate_script
from tools import save, Model
from use_cases_generator import generate_use_case


def main():
    user_prompt = input('Digite um caso de uso: ')

    use_cases = generate_use_case(user_prompt, Model.GPT_3_5)
    print(f'\nCaso de uso - Modelo padrão:\n{use_cases}')

    use_cases = generate_use_case(user_prompt, Model.GPT_FINE_TUNED)
    print(f'\nCaso de uso - Modelo fine tuned:\n{use_cases}')

    # test_scenario = generate_test_scenario(use_cases)
    # print(f'\nCenarios de teste:\n{test_scenario}')
    #
    # script_test = generate_script(use_cases, test_scenario)
    # print(f'\nScript teste:\n{script_test}')

    # save('data/script_test.py', script_test)


if __name__ == '__main__':
    main()
