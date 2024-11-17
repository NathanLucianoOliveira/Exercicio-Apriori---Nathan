import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from itertools import combinations

def transformar_dados_para_matriz_binaria(file_path):
    # Verifica a extensão do arquivo
    if file_path.endswith('.csv'):
        with open(file_path, 'r') as f:
            transactions = [line.strip().split(',') for line in f.readlines()]
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path, header=None)
        transactions = df.values.tolist()
    else:
        raise ValueError("Formato de arquivo não suportado. Use '.csv' ou '.xlsx'.")

    all_products = set(item for sublist in transactions for item in sublist if pd.notnull(item))

    data = []
    for transaction in transactions:
        transaction_data = {product: (product in transaction) for product in all_products}
        data.append(transaction_data)

    return pd.DataFrame(data)


def calcular_frequencia_produto(df):
    frequencias = df.sum()
    total_registros = len(df)
    frequencia_produto = frequencias / total_registros
    return frequencia_produto


def cortar_por_suporte(frequencia_produto, min_support):
    produtos_filtrados = frequencia_produto[frequencia_produto >= min_support]
    return produtos_filtrados


def gerar_combinacoes(produtos_filtrados):
    combinacoes = list(combinations(produtos_filtrados.index, 2))
    return combinacoes


def calcular_regras_associacao(df, combinacoes, min_confidence):
    regras = []
    for combinacao in combinacoes:
        df_subconjunto = df[df[combinacao[0]] & df[combinacao[1]]]
        count_comb = len(df_subconjunto)

        support_A = df[combinacao[0]].sum() / len(df)
        support_B = df[combinacao[1]].sum() / len(df)
        support_AB = count_comb / len(df)

        if support_A > 0 and support_B > 0:
            confidence = support_AB / support_A
            if confidence >= min_confidence:
                regras.append((combinacao, support_AB, confidence))
    return regras


def processar_csv(file_path, min_support=0.5, min_confidence=0.5):
    df = transformar_dados_para_matriz_binaria(file_path)

    frequencia_produto = calcular_frequencia_produto(df)
    print(f"Frequência de cada produto em {file_path}:")
    print(frequencia_produto)

    produtos_filtrados = cortar_por_suporte(frequencia_produto, min_support)
    print(f"Produtos após o corte de suporte em {file_path}:")
    print(produtos_filtrados)

    combinacoes = gerar_combinacoes(produtos_filtrados)
    print(f"Combinações de 2 produtos em {file_path}:")
    print(combinacoes)

    regras = calcular_regras_associacao(df, combinacoes, min_confidence)
    print(f"Regras de associação em {file_path}:")
    for regra in regras:
        print(f"Produtos: {regra[0]}, Suporte: {regra[1]:.4f}, Confiança: {regra[2]:.4f}")


# Atualize o caminho para o seu arquivo Excel
file_paths = ['C:/Users/natha/Desktop/Apriori-Exercicio/1-main/att1.xlsx']

for file_path in file_paths:
    processar_csv(file_path, min_support=0.5, min_confidence=0.5)
