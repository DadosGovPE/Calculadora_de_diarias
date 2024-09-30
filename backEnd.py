from datetime import datetime

# Função para calcular o valor das diárias
def calcular_diarias(data_ida, hora_ida, data_volta, hora_volta, valor_diaria_integral, valor_diaria_parcial):
    # Converte strings para objetos datetime
    data_hora_ida = datetime.strptime(f"{data_ida} {hora_ida}", "%Y-%m-%d %H:%M")
    data_hora_volta = datetime.strptime(f"{data_volta} {hora_volta}", "%Y-%m-%d %H:%M")

    # Calcula o número total de dias (diferença entre as datas)
    total_dias = (data_hora_volta.date() - data_hora_ida.date()).days

    # Verifica se a pessoa retorna após as 10:00 no dia da volta
    hora_limite = datetime.strptime(f"{data_volta} 10:00", "%Y-%m-%d %H:%M")

    # Inicializa contadores
    diarias_integrais = total_dias  # Assume todas as diárias inteiras inicialmente
    diarias_parciais = 0  # Inicializa o contador de diárias parciais

    # Verifica se a data de volta é um fim de semana
    data_volta_obj = data_hora_volta.date()
    dia_da_semana = data_volta_obj.weekday()  # 0 = segunda, 6 = domingo

    if dia_da_semana in [5, 6]:  # Sábado (5) ou Domingo (6)
        diarias_parciais = 0  # Se for fim de semana, não conta como parcial
    else:
        # Se retornar antes das 10:00 no último dia, um dia é parcial
        if data_hora_volta < hora_limite:
            diarias_integrais -= 1  # Retira um dia da contagem de diárias integrais
            diarias_parciais += 1  # Conta o último dia como parcial

    # Calcula o custo total usando o valor de diárias integrais e parciais definidos
    custo_total = (diarias_integrais * valor_diaria_integral) + (diarias_parciais * valor_diaria_parcial)

    return total_dias, diarias_integrais, diarias_parciais, custo_total

# Grupos e diárias
grupos = {
    "g1": [
        "vitória-es", "florianópolis-sc", "curitiba-pr", "boa vista-ro", "macapá-ap",
        "porto velho-ro", "rio branco-ac", "aracaju-se", "joão pessoa-pb", "maceió-al",
        "natal-rn", "salvador-ba", "são luís-ma", "teresina-pi", "campo grande-ms",
        "cuiabá-mt", "goiânia-go", "palmas-to"
    ],
    "g2": ["brasília-df", "manaus-am"],
    "g3": [
        "recife-pe", "cidades do interior de sergipe", "cidades do interior de alagoas",
        "cidades do interior de paraíba", "cidades do interior de rio grande do norte", "juazeiro-ba"
    ]
}

beneficiarios = {
    'b1': ['das', 'das1'],
    'b2': ['das2', 'das3', 'das4', 'das5', 'fda', 'fda4', 'caa1', 'caa5'],
    'b3': ['fgs-1', 'fgs-2', 'fgs-3', 'fga-1', 'fga-2', 'fga-3']
}

diarias = {
    "g1": {
        "b1": {"integral": 424.22, "parcial": 127.26},
        "b2": {"integral": 313.28, "parcial": 94.00},
        "b3": {"integral": 215.40, "parcial": 64.62}
    },
    "g2": {
        "b1": {"integral": 475.13, "parcial": 142.53},
        "b2": {"integral": 350.87, "parcial": 105.28},
        "b3": {"integral": 241.25, "parcial": 72.37}
    },
    "g3": {
        "b1": {"integral": 449.67, "parcial": 134.90},
        "b2": {"integral": 332.08, "parcial": 99.64},
        "b3": {"integral": 228.32, "parcial": 68.50}
    }
}

# Entrada do usuário
benef = input('Qual o seu símbolo? ').lower()

# Verificando se o beneficiário existe e obtendo o grupo de beneficiário
grupo_beneficiario = None

for grupo, ben_list in beneficiarios.items():
    if benef in ben_list:
        grupo_beneficiario = grupo
        break

if grupo_beneficiario is not None:
    destino = input('Qual o seu destino? ').lower()

    # Verificando em qual grupo de destino o local informado pertence
    grupo_destino = None
    for grupo, destinos in grupos.items():
        if destino in destinos:
            grupo_destino = grupo
            break

    if grupo_destino is not None:
        try:
            data_ida = input("Digite a data de ida (formato YYYY-MM-DD): ")
            hora_ida = input("Digite a hora de ida (formato HH:MM): ")
            data_volta = input("Digite a data de volta (formato YYYY-MM-DD): ")
            hora_volta = input("Digite a hora de volta (formato HH:MM): ")

            # Obtendo os valores de diárias integrais e parciais com base no grupo de destino e grupo de beneficiário
            valor_diaria_integral = diarias[grupo_destino][grupo_beneficiario]["integral"]
            valor_diaria_parcial = diarias[grupo_destino][grupo_beneficiario]["parcial"]

            # Calcula o total de dias e as diárias integrais e parciais
            total_dias, diarias_integrais, diarias_parciais, custo_total = calcular_diarias(
                data_ida, hora_ida, data_volta, hora_volta, valor_diaria_integral, valor_diaria_parcial
            )

            # Exibe os resultados
            print(f"\nTotal de dias: {total_dias}")
            print(f"Diárias integrais: {diarias_integrais}")
            print(f"Diárias parciais: {diarias_parciais}")
            print(f"Custo total: R$ {custo_total:.2f}")

        except ValueError:
            print("Data ou hora inserida inválida. Por favor, siga o formato correto.")
    else:
        print('Destino não encontrado no grupo.')
else:
    print('Beneficiário não encontrado.')
