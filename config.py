import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', '12345')

    # Configuração do banco de dados MySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', "mysql+pymysql://root:12345@localhost/cromo_financiamentos")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.environ.get('FLASK_DEBUG', 'False') == 'True'

    # Configuração para envio de e-mails
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
