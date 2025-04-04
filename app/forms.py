from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm # type: ignore
from wtforms import StringField, SubmitField # type: ignore
from wtforms.validators import DataRequired, Email, Length # type: ignore
from datetime import datetime

# Configuração do banco de dados
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///financiamento.db'
    app.config['SECRET_KEY'] = 'chave_secreta'
    db.init_app(app)
    return app

# Modelos
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.Text)

class PedidoFinanciamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parceiro_nome = db.Column(db.String(255))
    parceiro_email = db.Column(db.String(255))
    parceiro_cpf_cnpj = db.Column(db.String(20))
    cliente_nome = db.Column(db.String(255))
    estado_civil = db.Column(db.String(50))
    rg = db.Column(db.String(20))
    cpf = db.Column(db.String(20), unique=True, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    celular = db.Column(db.String(15))
    renda = db.Column(db.Numeric(10, 2))
    mae = db.Column(db.String(255))
    pai = db.Column(db.String(255))
    nacionalidade = db.Column(db.String(100))
    estado_residencia = db.Column(db.String(100))
    cidade_residencia = db.Column(db.String(100))
    classe_profissional = db.Column(db.String(100))
    profissao = db.Column(db.String(100))
    valor_patrimonial = db.Column(db.Numeric(10, 2))
    pep = db.Column(db.Boolean, default=False)
    fatca = db.Column(db.Boolean, default=False)
    telefones_adicionais = db.Column(db.Text, nullable=True)
    telefones_comerciais = db.Column(db.Text, nullable=True)
    referencia_nome = db.Column(db.String(255))
    referencia_telefone = db.Column(db.String(15))
    autonomo = db.Column(db.Boolean, default=False)
    referencia_comercial_nome = db.Column(db.String(255), nullable=True)
    referencia_comercial_telefone = db.Column(db.String(15), nullable=True)
    valor_financiamento = db.Column(db.Numeric(10, 2))
    tipo_bem = db.Column(db.String(20), nullable=False)
    marca = db.Column(db.String(100), nullable=True)
    modelo = db.Column(db.String(255), nullable=True)
    ano_fabricacao = db.Column(db.Integer, nullable=True)
    placa = db.Column(db.String(10), nullable=True)
    data_pedido = db.Column(db.DateTime, default=datetime.utcnow)

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    financiamento_id = db.Column(db.Integer, db.ForeignKey('financiamento.id'))
    data = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Em análise')

class Financiamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    valor = db.Column(db.Numeric(10, 2))
    prazo = db.Column(db.Integer)
    taxa_juros = db.Column(db.Numeric(5, 2))

# Formulário
class FinanciamentoForm(FlaskForm):
    parceiro_nome = StringField('Nome do Parceiro', validators=[DataRequired()])
    parceiro_email = StringField('E-mail do Parceiro', validators=[DataRequired(), Email()])
    cliente_nome = StringField('Nome do Cliente', validators=[DataRequired()])
    cpf_cliente = StringField('CPF do Cliente', validators=[DataRequired(), Length(min=11, max=14)])
    telefone = StringField('Celular', validators=[DataRequired()])
    renda = StringField('Renda', validators=[DataRequired()])
    valor_financiamento = StringField('Valor do Financiamento', validators=[DataRequired()])
    marca_veiculo = StringField('Marca do Veículo', validators=[DataRequired()])
    modelo_veiculo = StringField('Modelo do Veículo', validators=[DataRequired()])
    ano_fabricacao = StringField('Ano de Fabricação', validators=[DataRequired()])
    placa = StringField('Placa', validators=[DataRequired()])
    submit = SubmitField('Enviar')

# Rotas
app = create_app()
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solicitar', methods=['GET', 'POST'])
def solicitar():
    form = FinanciamentoForm()
    if form.validate_on_submit():
        novo_pedido = PedidoFinanciamento(
            parceiro_nome=form.parceiro_nome.data,
            parceiro_email=form.parceiro_email.data,
            cliente_nome=form.cliente_nome.data,
            cpf=form.cpf_cliente.data,
            celular=form.telefone.data,
            renda=form.renda.data,
            valor_financiamento=form.valor_financiamento.data,
            marca=form.marca_veiculo.data,
            modelo=form.modelo_veiculo.data,
            ano_fabricacao=form.ano_fabricacao.data,
            placa=form.placa.data
        )
        db.session.add(novo_pedido)
        db.session.commit()
        flash('Pedido enviado com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('solicitar.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)