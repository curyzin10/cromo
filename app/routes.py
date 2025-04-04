from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, PedidoFinanciamento
import requests

main = Blueprint('main', __name__)

# Chave secreta do reCAPTCHA
RECAPTCHA_SECRET_KEY = "6Lfd_QYrAAAAADDdUdYAjTT-b_A-mSwug4ihzIY3"

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/quem-somos')
def quem_somos():
    return render_template('quem-somos.html')

@main.route('/contatos')
def contatos():
    return render_template('contatos.html')

@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/veiculo', methods=['GET', 'POST'])
def veiculo():
    if request.method == 'POST':
        criar_pedido_financiamento('veiculo', request.form)
        return redirect(url_for('main.home'))
    return render_template('veiculo.html')

@main.route('/imovel', methods=['GET', 'POST'])
def imovel():
    if request.method == 'POST':
        recaptcha_response = request.form.get('g-recaptcha-response')
        recaptcha_verification = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": RECAPTCHA_SECRET_KEY, "response": recaptcha_response}
        ).json()

        if not recaptcha_verification.get("success"):
            flash("Erro na verificação do reCAPTCHA. Tente novamente.", "danger")
            return redirect(url_for('main.imovel'))

        criar_pedido_financiamento('imovel', request.form)
        return redirect(url_for('main.home'))
    return render_template('imovel.html')

@main.route('/embarcacao', methods=['GET', 'POST'])
def embarcacao():
    if request.method == 'POST':
        criar_pedido_financiamento('embarcacao', request.form)
        return redirect(url_for('main.home'))
    return render_template('embarcacao.html')

def criar_pedido_financiamento(tipo, dados):
    try:
        novo_pedido = PedidoFinanciamento(
            parceiro_nome=dados.get('parceiro_nome'),
            parceiro_email=dados.get('parceiro_email'),
            parceiro_cpf_cnpj=dados.get('parceiro_cpf_cnpj'),
            cliente_nome=dados.get('cliente_nome'),
            estado_civil=dados.get('estado_civil'),
            rg=dados.get('rg'),
            cpf=dados.get('cpf'),
            data_nascimento=datetime.strptime(dados.get('data_nascimento'), '%Y-%m-%d').date(),
            celular=dados.get('celular'),
            renda=float(dados.get('renda', 0)),
            mae=dados.get('mae'),
            pai=dados.get('pai'),
            nacionalidade=dados.get('nacionalidade'),
            estado_residencia=dados.get('estado_residencia'),
            cidade_residencia=dados.get('cidade_residencia'),
            classe_profissional=dados.get('classe_profissional'),
            profissao=dados.get('profissao'),
            valor_patrimonial=float(dados.get('valor_patrimonial', 0)),
            pep=dados.get('pep'),
            fatca=dados.get('fatca'),
            telefones_adicionais=dados.get('telefones_adicionais'),
            telefones_comerciais=dados.get('telefones_comerciais'),
            referencia_nome=dados.get('referencia_nome'),
            referencia_telefone=dados.get('referencia_telefone'),
            autonomo=dados.get('autonomo'),
            valor_financiamento=float(dados.get('valor_financiamento', 0))
        )

        if tipo in ['veiculo', 'embarcacao']:
            novo_pedido.marca = dados.get(f'marca_{tipo}')
            novo_pedido.modelo = dados.get(f'modelo_{tipo}')
            novo_pedido.ano_fabricacao = int(dados.get('ano_fabricacao', 0))
        
        if tipo == 'veiculo':
            novo_pedido.placa = dados.get('placa')

        db.session.add(novo_pedido)
        db.session.commit()
        flash("Pedido de financiamento enviado com sucesso!", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao processar o pedido: {str(e)}", "danger")

@main.route('/ver_pedidos')
def ver_pedidos():
    pedidos = PedidoFinanciamento.query.all()  # Sem usar 'with db.session()'
    return render_template('ver_pedidos.html', pedidos=pedidos)
