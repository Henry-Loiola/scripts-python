# -*- coding: utf-8 -*-
"""Analise_Taxa_CDI.ipy

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/102vwoVZ5lZSKZGrSwZwxoaSexAVEeXh6
"""

import os
import time
import json
from random import random
from datetime import datetime
import requests

# URL da taxa CDI
URL = 'https://cdi-generator.vercel.app/api'

# Verifica se o arquivo já existe; se não, cria com o cabeçalho
if not os.path.exists('./taxa-cdi.csv'):
    with open('./taxa-cdi.csv', mode='w', encoding='utf8') as fp:
        fp.write('data,hora,taxa\n')

# Loop para coletar dados 10 vezes
for _ in range(10):
    # Captura data e hora atual
    data_e_hora = datetime.now()
    data = datetime.strftime(data_e_hora, '%Y/%m/%d')
    hora = datetime.strftime(data_e_hora, '%H:%M:%S')

    # Captura a taxa CDI do site
    try:
        response = requests.get(URL,  verify=False)
        response.raise_for_status()
        dado = json.loads(response.text)
        cdi = float(dado['taxa'].replace(',', '.')) + (random() - 0.5)
    except requests.HTTPError:
        print("Dado não encontrado, continuando.")
        cdi = None
    except Exception as exc:
        print("Erro, parando a execução.")
        raise exc

    # Salva a taxa no CSV
    with open('./taxa-cdi.csv', mode='a', encoding='utf8') as fp:
        fp.write(f'{data},{hora},{cdi}\n')

    # Pausa para evitar sobrecarga no site
    time.sleep(2 + (random() - 0.5))

print("Extração concluída com sucesso!")

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Lê os dados do arquivo CSV
df = pd.read_csv('./taxa-cdi.csv')

# Cria o gráfico da taxa CDI ao longo do tempo
plt.figure(figsize=(10, 6))
grafico = sns.lineplot(x=df['hora'], y=df['taxa'])
grafico.set_xticklabels(labels=df['hora'], rotation=90)
plt.title("Taxa CDI ao longo do tempo")
plt.xlabel("Hora")
plt.ylabel("Taxa CDI")

# Salva e exibe o gráfico
plt.savefig("grafico_cdi.png")
plt.show()

