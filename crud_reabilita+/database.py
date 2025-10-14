import sqlite3

def conectar():
    """Conecta ao banco de dados SQLite e o retorna."""
    conn = sqlite3.connect('reabilita.db')
    return conn

def criar_tabela_usuarios():
    """Cria a tabela de usuários se ela não existir."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            cpf TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            cartao_sus TEXT NOT NULL,
            cep TEXT NOT NULL,
            complemento TEXT,
            senha TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    criar_tabela_usuarios()
    print("Banco de dados e tabela de usuários criados com sucesso.")