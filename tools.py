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
