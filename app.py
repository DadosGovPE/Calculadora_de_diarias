from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route('/')

def index():
    cargos = ['DAS','DAS1','DAS-2', 'DAS-3', 'DAS-4', 'DAS-5','FDA','FDA-1','FDA-2','FDA-3','FDA-4','CAA-1','CAA-2',
         'CAA-3','CAA-4','CAA-5','FGS-1','FGS-2','FGS-3', 'FGA-1','FGA-2','FGA-3']
    
    return render_template('index.html', cargos=cargos)


@app.route('/cargo/<cargo>')
def cargo_page(cargo):
    beneficiarios = {
        'b1': ['das', 'das1'],
        'b2': ['das2', 'das3', 'das4', 'das5', 'fda', 'fda4', 'caa1', 'caa5'],
        'b3': ['fgs-1', 'fgs-2', 'fgs-3', 'fga-1', 'fga-2', 'fga-3']
    }
    
    for chave, valor in beneficiarios.items():
        if cargo in valor:
            if chave == "b3":
                resposta = input("Seu cargo possui nível superior (sim/não)? ").lower()
                if resposta == "sim":
                    chave_destino = "b2"
                else:
                    chave_destino = "b3"
            else:
                chave_destino = chave
            
            # Renderizar o template passando a chave e o cargo
            return render_template('qual_destino.html', chave=chave_destino, cargo=cargo)
    
    return "Cargo não encontrado", 404

@app.route('/destino/<destino>')
def destino_page(destino):
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
    
    # Verifica o destino e obtém a chave correspondente
    for chave, valor in destinos.items():
        if destino in valor:
            # Renderiza o template com a chave e destino
            return render_template('data_hora.html', chave=chave, destino=destino)
    
    # Se o destino não for encontrado, pode retornar uma mensagem ou redirecionar
    return "Destino não encontrado", 404





@app.route('/calcular_diarias', methods=['POST'])
def calcular_diarias():
    # Obter dados do formulário
    data_hora_de_chegada_ao_destino = datetime.strptime(request.form['data_chegada'], '%Y-%m-%d %H:%M')
    data_hora_de_saida = datetime.strptime(request.form['data_saida'], '%Y-%m-%d %H:%M')
    grupo_cargo = request.form['grupo_cargo']
    grupo_destino = request.form['grupo_destino']

    duracao = data_hora_de_saida - data_hora_de_chegada_ao_destino
    valor_total = 0

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

    # Se for uma viagem de mais de um dia
    if duracao.days > 0:
        valor_total += diarias[grupo_cargo][grupo_destino]['integral'] * (duracao.days - 1)

        # Calcula o último dia com base na hora da saída
        if data_hora_de_saida.hour < 10:  # Último dia conta como parcial
            eh_feriado = request.form['feriado'].lower()  # "sim" ou "não"
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

    # Renderiza o template com o resultado
    return render_template('resultado.html', valor_total=valor_total)

if __name__ == '__main__':
    app.run(debug=True)


    



    