import pymysql
from config.settings import IP_HOST, USUARIO, SENHA, BANCO

class Looqbox_BD:

    def __init__(self):

        self.conexao = None
        self.cursor = None
        self.conectar_ao_banco()

    def conectar_ao_banco(self):

        try:
            self.conexao = pymysql.connect(
                host =      IP_HOST,
                user =      USUARIO,
                password =  SENHA,
                database =  BANCO,
            )
            self.cursor = self.conexao.cursor()
        except Exception as error:
            print(f'[Erro] Falha ao conectar-se ao banco de dados: {error}')
            return

    def encerrar_conexao_ao_banco(self):
        
        if not self.conexao:
            print(f'[Aviso] Não há conexão ativa com o banco de dados!')
            return
        
        self.conexao.close()
        print(f'[Sucesso] Conexão com o banco de dados encerrada!')
        