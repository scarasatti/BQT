import os
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

    print(f"Questão salva em: {caminho} (sobrescrita)")
    subir_para_o_firebase()
def buscar_questoes(materia=None, dificuldade=None, tempo_execucao=None):
    print("\n🔎 Buscando questões com os filtros:")
    filtros = []
    colecao = db.collection("questoes")

    if materia:
        colecao = colecao.where("materia", "==", materia)
        filtros.append(f"Matéria: {materia}")
    if dificuldade:
        colecao = colecao.where("dificuldade", "==", dificuldade)
        filtros.append(f"Dificuldade: {dificuldade}")
    if tempo_execucao:
        colecao = colecao.where("tempo_execucao", "==", tempo_execucao)
        filtros.append(f"Tempo: {tempo_execucao} min")

    print(", ".join(filtros) if filtros else "Sem filtros — buscando todas as questões")

    resultados = colecao.stream()
    questoes = []

    for doc in resultados:
        dados = doc.to_dict()
        questoes.append(dados)
        print(f"\n📝 Enunciado: {dados.get('enunciado')}")
        print(f"Tipo: {dados.get('tipo')}")
        print(f"Matéria: {dados.get('materia')}")
        print(f"Dificuldade: {dados.get('dificuldade')}")
        print(f"Tempo: {dados.get('tempo_execucao')} min")

    if not questoes:
        print("❌ Nenhuma questão encontrada com os filtros aplicados.")

    return questoes


if __name__ == "__main__":
    opcao = input("Escolha uma opção:\n1 - Criar nova questão\n2 - Buscar questões\n> ").strip()

    if opcao == "1":
        criar_questao()
    elif opcao == "2":
        materia = input("Filtrar por matéria (ou deixe em branco): ").strip() or None
        dificuldade = input("Filtrar por dificuldade (1, 2, 3 - ou deixe em branco): ").strip()
        dificuldade = int(dificuldade) if dificuldade else None
        tempo = input("Filtrar por tempo de execução (em minutos - ou deixe em branco): ").strip()
        tempo = int(tempo) if tempo else None

        buscar_questoes(materia, dificuldade, tempo)

