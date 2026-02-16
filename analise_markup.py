import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def gerar_cenario(ano, markup, vendas_por_mes, custo_medio, custo_fixo_mensal):
    
    lista_vendas = []
    
    for mes in range(1, 13):
        
        for venda in range(vendas_por_mes):
            
            custo_unitario = int(np.random.normal(custo_medio, 10))
            preco_unitario = custo_unitario * markup
            
            data_venda = pd.Timestamp(
                year=ano,
                month=mes,
                day=np.random.randint(1, 28)
            )
            
            lista_vendas.append({
                'data_venda': data_venda,
                'ano': ano,
                'mes': mes,
                'custo_unitario': custo_unitario,
                'markup': markup,
                'preco_unitario': preco_unitario,
                'quantidade': 1
            })
    
    dados = pd.DataFrame(lista_vendas)
    
    dados['receita'] = dados['preco_unitario'] * dados['quantidade']
    dados['custo_total'] = dados['custo_unitario'] * dados['quantidade']
    dados['lucro_bruto'] = dados['receita'] - dados['custo_total']
    
    # Lucro líquido mensal
    lucro_mensal = dados.groupby('mes')['lucro_bruto'].sum()
    lucro_liquido_mensal = lucro_mensal - custo_fixo_mensal
    
    lucro_liquido_total = lucro_liquido_mensal.sum()
    
    return dados, lucro_liquido_total


# CENÁRIO 2024
dados_2024, lucro_2024 = gerar_cenario(
    ano=2024,
    markup=3.0,
    vendas_por_mes=500,
    custo_medio=80,
    custo_fixo_mensal=40000
)

# CENÁRIO 2025 (elasticidade aplicada)
dados_2025, lucro_2025 = gerar_cenario(
    ano=2025,
    markup=2.5,
    vendas_por_mes=int(500 * 1.25),
    custo_medio=80,
    custo_fixo_mensal=40000
)

print("Lucro Líquido 2024:", lucro_2024)
print("Lucro Líquido 2025:", lucro_2025)
print("Diferença:", lucro_2025 - lucro_2024)

aumentos = np.arange(0, 0.6, 0.05)  # de 0% até 55%
lucros_2025 = []

for aumento in aumentos:
    
    vendas = int(500 * (1 + aumento))
    
    _, lucro = gerar_cenario(
        ano=2025,
        markup=2.5,
        vendas_por_mes=vendas,
        custo_medio=80,
        custo_fixo_mensal=40000
    )
    
    lucros_2025.append(lucro)


plt.figure()
plt.plot(aumentos * 100, lucros_2025)
plt.axhline(y=lucro_2024)

plt.xlabel("Aumento de Volume (%)")
plt.ylabel("Lucro Líquido")
plt.title("Análise de Sensibilidade - Volume vs Lucro")

plt.show()
