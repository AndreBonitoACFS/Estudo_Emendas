import pandas as pd
import sys
import os
import ast
import matplotlib.pyplot as plt

# Verifica argumento
if len(sys.argv) < 2:
    print("❌ Por favor, informe o número do artigo como argumento.")
    sys.exit(1)

numero_artigo = sys.argv[1].strip()

# Carrega planilha
df = pd.read_excel(r'C:\Users\usuário\Documents\PLP 108\PLP 108 - com artigos.xlsx')

# Garante que seja lista válida
df['artigos_mencionados'] = df['artigos_mencionados'].apply(
    lambda x: ast.literal_eval(x) if isinstance(x, str) else (x if isinstance(x, list) else [])
)

# Filtro por igualdade exata como string
df_filtrado = df[
    df['artigos_mencionados'].apply(
        lambda lista: any(str(item) == numero_artigo for item in lista)
    )
]

# Cria pastas de saída
excel_dir = 'Excels_Gerados'
grafico_dir = 'Graficos_Gerados'
os.makedirs(excel_dir, exist_ok=True)
os.makedirs(grafico_dir, exist_ok=True)

# Salva Excel
nome_excel = f"{excel_dir}/resultado_artigo_{numero_artigo}.xlsx"
df_filtrado.to_excel(nome_excel, index=False)

# Gera gráfico se houver dados
if len(df_filtrado) > 0:
    print(f"\n✅ Excel salvo: {nome_excel}")
    print(f"🔎 Total de linhas exportadas: {len(df_filtrado)}")

    # Contagem de emendas ordenada da maior para a menor
    contagem = df_filtrado['Emenda'].value_counts().sort_values(ascending=False)

    # Gera gráfico
    plt.figure(figsize=(10, 6))
    contagem.plot(kind='bar')
    plt.title(f"Emendas que mencionam o artigo {numero_artigo}")
    plt.xlabel("Emenda")
    plt.ylabel("Ocorrências")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.grid(axis='y')

    # Salva gráfico
    nome_grafico = f"{grafico_dir}/grafico_artigo_{numero_artigo}.png"
    plt.savefig(nome_grafico)
    plt.close()

    print(f"📊 Gráfico salvo: {nome_grafico}")
else:
    print(f"\n⚠️ Nenhuma linha encontrada com artigo '{numero_artigo}'.")
