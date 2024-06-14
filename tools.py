import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()


class Model(Enum):
    GPT_3_5 = 'gpt-3.5-turbo'
    GPT_4O = 'gpt-4o'
    GPT_FINE_TUNED = os.getenv('FINE_TUNED_MODEL')


def load(filename):
    try:
        with open(filename, "r") as file:
            data = file.read()
            return data
    except IOError as e:
        print(f"Erro no carregamento do arquivo: {e}")


def save(filename, content):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")
