from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()  # ✅ Defina `db` aqui mesmo

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.Text)

class PedidoFinanciamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_nome = db.Column(db.String(255))
    cpf = db.Column(db.String(20), unique=True, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    celular = db.Column(db.String(15))
    valor_financiamento = db.Column(db.Numeric(10, 2))
    tipo_bem = db.Column(db.String(20), nullable=False)
    marca = db.Column(db.String(100), nullable=True)
    modelo = db.Column(db.String(255), nullable=True)
    ano_fabricacao = db.Column(db.Integer, nullable=True)
    placa = db.Column(db.String(10), nullable=True)
    data_pedido = db.Column(db.DateTime, default=datetime.utcnow)

