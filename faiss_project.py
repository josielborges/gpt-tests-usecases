import json
import os

import faiss
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

from embedding_generator import generate_embedding

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

FAISS_INDEX_SIZE = 1536  # to text-embedding-3-small, to text-embedding-3-large use 3072
DOCUMENTS_DIRECTORY = 'AcordeLab'
FAISS_DATA_PATH = 'project.index'
METADATA_PATH = 'project_metadata.json'


def read_create_faiss_index(file_path, array_size):
    if os.path.exists(file_path):
        print('\nÍndice já existe, carregando...')
        return faiss.read_index(file_path)
    else:
        print('\nCriando novo indice...')
        return faiss.IndexFlatL2(array_size)


def create_faiss_data(faiss_data_path, descriptions, metadata, metadata_path):
    faiss_data = read_create_faiss_index(faiss_data_path, FAISS_INDEX_SIZE)

    if not os.path.exists(faiss_data_path):
        faiss_data = add_embedding_index(faiss_data, descriptions, metadata, metadata_path)
        faiss.write_index(faiss_data, faiss_data_path)

    return faiss_data


def add_embedding_index(faiss_data, descriptions, metadata, metadata_path):
    embeddings = np.array([generate_embedding(text) for text in descriptions]).astype(np.float32)
    faiss.normalize_L2(embeddings)
    faiss_data.add(embeddings)

    with open(metadata_path, 'w', encoding='utf-8') as file:
        json.dump(metadata, file, ensure_ascii=False)

    return faiss_data


def get_similar_documents(search_text, faiss_data, metadata_path, results=1):
    search_text_embedding = np.array([generate_embedding(search_text)]).astype(np.float32)
    faiss.normalize_L2(search_text_embedding)
    D, I = faiss_data.search(search_text_embedding, results)

    with open(metadata_path, 'w', encoding='utf-8') as file:
        metadata = json.load(file)

    for i in range(results):
        index = I[0][i]
        print(f"\nSimilaridade {i + 1}: {D[0][i]}")
        print(f"Documento: {metadata[index]['document']}")
        print(f"Texto: {metadata[index]['meta_description']}")

    found_document = ''

    if metadata[I[0][0]].get('path'):
        found_document = metadata[I[0][0]].get('path')

    return found_document
