from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta


app = Flask(__name__)
app.secret_key = 'babi'
  # Necessário para usar a sessão
grupos = {

    "g1": [    "Vitória-ES", "Florianópolis-SC", "Curitiba-PR", "Boa Vista-RO", 
    "Macapá-AP", "Porto Velho-RO", "Rio Branco-AC", "Aracaju-SE", 
    "João Pessoa-PB", "Maceió-AL", "Natal-RN", "Salvador-BA", 
    "São Luís-MA", "Teresina-PI", "Campo Grande-MS", "Cuiabá-MT", 
    "Goiânia-GO", "Palmas-TO"],

    "g2": ["Brasília-DF", "Manaus-AM"],

    "g3": ["São Paulo-SP", "Rio de Janeiro-RJ", "Belo Horizonte-MG", 
        "Porto Alegre-RS", "Belém-PA", "Fortaleza-CE"],

    "g4": ["Recife e cidades do interior de Pernambuco", "Interior de Sergipe", " Interior de Alagoas", 
        "Interior da Paraíba", "Interior do Rio Grande do Norte", "Interior da Bahia"],

    "g5": ["Outros"]
}
beneficiarios = {
    'b1': ['das', 'das1'],
    'b2': ['das2', 'das3', 'das4', 'das5', 'fda', 'fda4', 'caa1', 'caa5'],
    'b3': ['fgs-1', 'fgs-2', 'fgs-3', 'fga-1', 'fga-2', 'fga-3', 'outros']
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

        "b1": {"integral": 449.67, "parcial": 137.90},

        "b2": {"integral": 332.08, "parcial": 99.64},

        "b3": {"integral": 228.32, "parcial": 68.50}

    },

    "g4": {

        "b1": {"integral": 339.36, "parcial": 101.80},

        "b2": {"integral": 250.62, "parcial": 75.20},

        "b3": {"integral": 172.32, "parcial": 57.00}

    },

    "g5": {

        "b1": {"integral": 241.86, "parcial": 72.54},

        "b2": {"integral": 170.12, "parcial": 57.00},

        "b3": {"integral": 120.00, "parcial": 55.00}

    }

}

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html')

@app.route('/multi_step_form', methods=['GET', 'POST'])
def multi_step_form():
    if request.method == 'POST':
        step = request.form.get('step')

        # Etapa 1: Captura o símbolo, verifica o ensino superior e o patrocínio
        if step == "1":
            simbolo_selecionado = request.form.get('simbolo').lower()
            ensino_superior = request.form.get('ensino_superior') == 'on'
            patrocinio = request.form.get('patrocinio') == 'on'  # Verifica se está patrocinado

            if simbolo_selecionado in beneficiarios['b1']:
                beneficiario = 'b1'
            elif simbolo_selecionado in beneficiarios['b3']:
                beneficiario = 'b2' if ensino_superior else 'b3'
            else:
                beneficiario = 'b2'

            # Armazenar o beneficiário e o patrocínio na sessão
            session['simbolo'] = simbolo_selecionado
            session['beneficiario'] = beneficiario
            session['patrocinio'] = patrocinio  # Armazena a escolha do patrocínio

            return render_template('destino.html', grupos=grupos)

        # Etapa 2: Captura o destino
        elif step == "2":
            destino = request.form.get('destino')
            session['destino'] = destino
            return render_template('hora_data.html')

        # Etapa 3: Captura as datas e horários
        elif step == "3":
            data_ida = request.form.get('data_ida')
            hora_ida = request.form.get('hora_ida')
            data_volta = request.form.get('data_volta')
            hora_volta = request.form.get('hora_volta')

            # Armazenar as informações de data/hora na sessão
            session['data_ida'] = data_ida
            session['hora_ida'] = hora_ida
            session['data_volta'] = data_volta
            session['hora_volta'] = hora_volta

            # Determinar o grupo do destino
            destino = session.get('destino')
            grupo = None
            for key, destinos in grupos.items():
                if destino in destinos:
                    grupo = key
                    break

            if grupo:
                beneficiario = session.get('beneficiario')
                valor_diaria_integral = diarias[grupo][beneficiario]["integral"]
                valor_diaria_parcial = diarias[grupo][beneficiario]["parcial"]

                # Verifica se a pessoa é patrocinada
                patrocinio = session.get('patrocinio', False)

                if patrocinio:
                    # Se patrocinado, todas as diárias são parciais
                    total_dias, diarias_integrais, diarias_parciais, custo_total = calcular_diarias_parcial(
                        data_ida, hora_ida, data_volta, hora_volta, valor_diaria_parcial
                    )
                else:
                    # Calcular as diárias normalmente
                    total_dias, diarias_integrais, diarias_parciais, custo_total = calcular_diarias(
                        data_ida, hora_ida, data_volta, hora_volta, valor_diaria_integral, valor_diaria_parcial
                    )

                # Armazenar os valores calculados na sessão
                session['total_dias'] = total_dias
                session['diarias_integrais'] = diarias_integrais
                session['diarias_parciais'] = diarias_parciais
                session['custo_total'] = custo_total

                # Passar as informações para o template de resumo
                return render_template('resumo.html',
                                   total_dias=session['total_dias'],
                                    diarias_integrais=session['diarias_integrais'],
                                    diarias_parciais=session['diarias_parciais'],
                                    custo_total=session['custo_total'],
                                    simbolo=session['simbolo'],
                                    destino=session['destino'],
                                    data_ida=session['data_ida'],
                                    hora_ida=session['hora_ida'],
                                    data_volta=session['data_volta'],
                                    hora_volta=session['hora_volta'])
            else:
                return "Destino não encontrado.", 400

        # Etapa 4: Finalização e confirmação
        elif step == "4":
            # Etapa final (após confirmação do usuário)
            return redirect(url_for('index'))

    # Caso contrário, redireciona para o início
        return redirect(url_for('index'))
    
    # Gerenciar as transições entre as páginas de acordo com o passo atual
    step = request.args.get('step', '1')
    
    if step == '1':
        simbolos = ['DAS', 'DAS1', 'DAS-2', 'DAS-3', 'DAS-4', 'DAS-5', 'FDA', 'FDA-1', 'FDA-2', 'FDA-3', 'FDA-4', 'CAA-1', 'CAA-2',
                    'CAA-3', 'CAA-4', 'CAA-5', 'FGS-1', 'FGS-2', 'FGS-3', 'FGA-1', 'FGA-2', 'FGA-3','OUTROS' ]
        return render_template('qual_sua_funcao.html', simbolos=simbolos)
    
    elif step == '2':
        return render_template('destino.html', grupos=grupos)
    
    elif step == '3':
        return render_template('hora_data.html')
    
    elif step == '4':
        return render_template('resumo.html', total_dias=session['total_dias'], 
                               diarias_integrais=session['diarias_integrais'], 
                               diarias_parciais=session['diarias_parciais'], 
                               custo_total=session['custo_total'])

    elif step == '5':
        return f"Cálculo finalizado! O custo total das diárias foi R${session['custo_total']:.2f}"

    return redirect(url_for('multi_step_form', step=1))


# Funções auxiliares
def determine_beneficiario(simbolo, ensino_superior):
    if simbolo in beneficiarios['b1']:
        return 'b1'
    elif simbolo in beneficiarios['b3']:
        if ensino_superior:
            return 'b2'
        return 'b3'
    return 'b2'

def determine_grupo(destino):
    for key, destinos in grupos.items():
        if destino in destinos:
            return key
    return None

# Função para calcular o valor das diárias
from datetime import datetime

# Função para calcular o valor das diárias
def calcular_diarias(data_ida, hora_ida, data_volta, hora_volta, valor_diaria_integral, valor_diaria_parcial):
    data_hora_ida = datetime.strptime(f"{data_ida} {hora_ida}", "%Y-%m-%d %H:%M")
    data_hora_volta = datetime.strptime(f"{data_volta} {hora_volta}", "%Y-%m-%d %H:%M")

    # Diferença de dias totais
    total_dias = (data_hora_volta.date() - data_hora_ida.date()).days

    # Verifica se os dias de ida ou volta são sábado (5) ou domingo (6)
    is_ida_fim_de_semana = data_hora_ida.weekday() >= 5  # 5 = Sábado, 6 = Domingo
    is_volta_fim_de_semana = data_hora_volta.weekday() >= 5

    # Se a viagem for no mesmo dia
    if total_dias == 0:
        # Verifica se é final de semana para contar como integral
        if is_ida_fim_de_semana or is_volta_fim_de_semana:
            diarias_integrais = 1
            diarias_parciais = 0
        else:
            diarias_integrais = 0
            diarias_parciais = 1
    else:
        # Se a viagem dura mais de um dia
        diarias_integrais = total_dias  # Assume todos os dias são integrais
        diarias_parciais = 1  # O último dia será sempre parcial, inicialmente

        # Verifica se a hora de volta é antes das 10:00 e ajusta as diárias integrais/parciais
        if data_hora_volta.hour < 10:
            diarias_integrais -= 1
            diarias_parciais += 1

        # Se o último dia for fim de semana (sábado ou domingo), será integral
        if is_volta_fim_de_semana:
            diarias_integrais += 1  # Último dia passa a ser integral
            diarias_parciais = 0  # Não há mais diárias parciais

    # Calcular o custo total com base nas diárias integrais e parciais
    custo_total = (diarias_integrais * valor_diaria_integral) + (diarias_parciais * valor_diaria_parcial)

    return total_dias+1 , diarias_integrais, diarias_parciais, custo_total

def calcular_diarias_parcial(data_ida, hora_ida, data_volta, hora_volta, valor_diaria_parcial):
    data_hora_ida = datetime.strptime(f"{data_ida} {hora_ida}", "%Y-%m-%d %H:%M")
    data_hora_volta = datetime.strptime(f"{data_volta} {hora_volta}", "%Y-%m-%d %H:%M")

    # Diferença de dias totais
    total_dias = (data_hora_volta.date() - data_hora_ida.date()).days + 1  # +1 para incluir o último dia

    # Todas as diárias serão parciais
    diarias_integrais = 0
    diarias_parciais = total_dias

    # Calcular o custo total com base nas diárias parciais
    custo_total = diarias_parciais * valor_diaria_parcial

    return total_dias, diarias_integrais, diarias_parciais, custo_total


if __name__ == '__main__':
    app.run(debug=True)