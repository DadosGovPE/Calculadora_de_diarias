from datetime import datetime

beneficiarios = {
    'b1': ['das', 'das1'],
    'b2': ['das2', 'das3', 'das4', 'das5', 'fda', 'fda4', 'caa1', 'caa5'],
    'b3': ['fgs-1', 'fgs-2', 'fgs-3', 'fga-1', 'fga-2', 'fga-3']
}

destinos = {
    "g1": [
        "vitória-es", "florianópolis-sc", "curitiba-pr", "boa vista-ro", "macapá-ap",
        "porto velho-ro", "rio branco-ac", "aracaju-se", "joão pessoa-pb", "maceió-al",
        "natal-rn", "salvador-ba", "são luís-ma", "teresina-pi", "campo grande-ms",
        "cuiabá-mt", "goiânia-go", "palmas-to"
    ],
    "g2": ["brasília-df", "manaus-am"],
    "g4": [
        "recife-pe", "cidades do interior de sergipe", "cidades do interior de alagoas",
        "cidades do interior de paraíba", "cidades do interior de rio grande do norte", "juazeiro-ba"
    ],
    "g3": ["são paulo - sp", "rio de janeiro-rj", "belo horizonte-mg", "porto alegre -rs", "belém-pa", "fortaleza-ce"],
    "g5": ["outros"]
}

diarias = {
    "b1": {
        "g1": {"integral": 424.22, "parcial": 127.26},
        "g2": {"integral": 313.28, "parcial": 94.00},
        "g3": {"integral": 215.40, "parcial": 64.62},
        "g4": {"integral": 339.36, "parcial": 101.80},
        "g5": {"integral": 241.86, "parcial": 72.54}
    },
    "b2": {
        "g1": {"integral": 475.13, "parcial": 142.53},
        "g2": {"integral": 350.87, "parcial": 105.28},
        "g3": {"integral": 241.25, "parcial": 72.37},
        "g4": {"integral": 250.62, "parcial": 75.20},
        "g5": {"integral": 170.12, "parcial": 57.00}
    },
    "b3": {
        "g1": {"integral": 449.67, "parcial": 134.90},
        "g2": {"integral": 332.08, "parcial": 99.64},
        "g3": {"integral": 228.32, "parcial": 68.50},
        "g4": {"integral": 172.30, "parcial": 57.00},
        "g5": {"integral": 120.00, "parcial": 55.00}
    }
}

def grupo_cargo(cargo):
    for chave, valor in beneficiarios.items():
        if cargo in valor:
            if chave == "b3":
                resposta = input("Seu cargo possui nível superior (sim/não)? ").lower()
                if resposta == "sim":
                    return "b2"
                else:
                    return "b3"
            return chave
    

def grupo_destino(destino):
    for chave, valor in destinos.items():
        if destino in valor:
            return chave
    return "g5"

def calcular_diarias(data_hora_de_chegada_ao_destino, data_hora_de_saida, grupo_cargo, grupo_destino):
    duracao = data_hora_de_saida - data_hora_de_chegada_ao_destino
    valor_total = 0

    # Se for uma viagem de mais de um dia
    if duracao.days > 0:
        # Adiciona diárias integrais para os dias completos (menos o último)
        valor_total += diarias[grupo_cargo][grupo_destino]['integral'] * (duracao.days - 1)

        # Calcula o último dia com base na hora da saída
        if data_hora_de_saida.hour < 10:  # Último dia conta como parcial, exceto se for sábado, domingo ou feriado
            eh_feriado = input("O dia de saída é feriado? (sim/não): ").lower()
            dia_semana_saida = data_hora_de_saida.weekday()  # 5 = sábado, 6 = domingo
            
            if eh_feriado == "sim" or dia_semana_saida in [5, 6]:  # Se for feriado, sábado ou domingo
                valor_total += diarias[grupo_cargo][grupo_destino]['integral']
            else:
                valor_total += diarias[grupo_cargo][grupo_destino]['parcial']
        else:  # Último dia conta como integral
            valor_total += diarias[grupo_cargo][grupo_destino]['integral']
    else:  # Se for no mesmo dia
        if data_hora_de_saida.hour < 10:  # Se a saída for antes das 10h, conta como parcial
            valor_total += diarias[grupo_cargo][grupo_destino]['parcial']
        else:  # Se for depois das 10h, conta como integral
            valor_total += diarias[grupo_cargo][grupo_destino]['integral']

    return valor_total

# Entrada de dados
beneficio = input('Qual seu cargo? ').lower()
grupo_cargo = grupo_cargo(beneficio)
destino = input('Qual seu destino? ').lower()
grupo_destino = grupo_destino(destino)

# Entradas de data e hora
data_hora_de_chegada_ao_destino = input("Digite a data e a hora de chegada ao destino no formato DD/MM/AAAA HH:MM: ")
data_hora_de_chegada_ao_destino = datetime.strptime(data_hora_de_chegada_ao_destino, "%d/%m/%Y %H:%M")

data_hora_de_saida = input("Digite a data e a hora de saída no formato DD/MM/AAAA HH:MM: ")
data_hora_de_saida = datetime.strptime(data_hora_de_saida, "%d/%m/%Y %H:%M")

# Chamada à função corrigida
valor_total = calcular_diarias(data_hora_de_chegada_ao_destino, data_hora_de_saida, grupo_cargo, grupo_destino)
print(f"O valor total das diárias é: {valor_total}")
