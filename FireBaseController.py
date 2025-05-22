import json
import firebase_admin
from firebase_admin import credentials, firestore

# Carrega a chave do Firebase
cred = credentials.Certificate("secrets/chave-firebase.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def subir_para_o_firebase():
    # Carrega a questão do arquivo JSON
    with open("questoes/questao_temp.json", encoding="utf-8") as f:
        dados = json.load(f)

    # Envia para a coleção "questoes"
    db.collection("questoes").add(dados)

    print("Questão enviada com sucesso.")
