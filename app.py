from flask import Flask, render_template, url_for
from datetime import datetime

app = Flask(__name__)

@app.route('/')

def index():
    cargos = ['DAS','DAS1','DAS-2', 'DAS-3', 'DAS-4', 'DAS-5','FDA','FDA-1','FDA-2','FDA-3','FDA-4','CAA-1','CAA-2',
         'CAA-3','CAA-4','CAA-5','FGS-1','FGS-2','FGS-3', 'FGA-1','FGA-2','FGA-3']
    
    return render_template('index.html', cargos=cargos)


@app.route('/cargo/<cargo>')
def cargo_page(cargo):
    # Definir os grupos de cargos
    b1 = ['DAS', 'DAS1']
    b2 = ['DAS-2', 'DAS-3', 'DAS-4', 'DAS-5', 'FDA', 'FDA-1', 'FDA-2', 'FDA-3', 'FDA-4', 
               'CAA-1', 'CAA-2', 'CAA-3', 'CAA-4', 'CAA-5']
    b3 = ['FGS-1', 'FGS-2', 'FGS-3', 'FGA-1', 'FGA-2', 'FGA-3']
    
    # Redirecionar para páginas diferentes com base no grupo
    if cargo in b1:
        return render_template('qual_destino.html', cargo=cargo)
    elif cargo in b2:
        return render_template('qual_destino.html', cargo=cargo)
    elif cargo in b3:
        return render_template('Possui_superior.html', cargo=cargo)
    else:
        return "Cargo não encontrado", 404


if __name__ == '__main__':
    app.run(debug='True')