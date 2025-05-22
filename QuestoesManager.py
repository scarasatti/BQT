import json
import os
from uuid import uuid4
from FireBaseController import *

def setar_tipo():
    escolha = int(input("Escolha o Tipo da questão: \n 1: Multipla_escolha\n 2: Dissertativa\n  3: Verdadeiro_falso): ").strip())
    if escolha == 1:
        tipo = "multipla_escolha"
        return tipo.strip()
    if escolha == 2:
        tipo = "dissertativa"
        return tipo.strip()
    if escolha == 3:
        tipo = "verdadeiro_falso"
        return tipo.strip()

def criar_questao():
    print("\n📌 Cadastro de nova questão\n")

    enunciado = input("Enunciado: ").strip()
    tipo = setar_tipo()
    print(tipo)
    dificuldade = int(input("Dificuldade (1-3): ").strip())
    serie = input("Série (ex: 5º ano): ").strip()
    materia = input("Matéria: ").strip()
    tempo_execucao = int(input("Tempo estimado (min): ").strip())

    alternativas = []
    resposta_correta = ""

    if tipo == "multipla_escolha":
        qtde = int(input("Quantas alternativas? "))
        for i in range(qtde):
            alt = input(f"Alternativa {i+1}: ").strip()
            alternativas.append(alt)
        resposta_correta = input("Resposta correta: ").strip()

    elif tipo == "verdadeiro_falso":
        alternativas = ["Verdadeiro", "Falso"]
        resposta_correta = input("Resposta correta (Verdadeiro/Falso): ").strip()

    elif tipo == "dissertativa":
        resposta_correta = ""

    else:
        print("❌ Tipo inválido.")
        return

    questao = {
        "enunciado": enunciado,
        "tipo": tipo,
        "alternativas": alternativas,
        "resposta_correta": resposta_correta,
        "dificuldade": dificuldade,
        "serie": serie,
        "materia": materia,
        "tempo_execucao": tempo_execucao
    }

    os.makedirs("questoes", exist_ok=True)
    caminho = os.path.join("questoes", "questao_temp.json")

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(questao, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Questão salva em: {caminho} (sobrescrita)")
    subir_para_o_firebase()

if __name__ == "__main__":
    criar_questao()
