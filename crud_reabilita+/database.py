import sqlite3

def conectar():
    """Conecta ao banco de dados SQLite e o retorna."""
    conn = sqlite3.connect('reabilita.db')
    return conn

def criar_tabela_usuarios():
    """Cria a tabela de usuários se ela não existir, agora alinhada com o front-end."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            cpf TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            telefone TEXT,
            nascimento TEXT,
            deficiencia TEXT,
            cep TEXT NOT NULL,
            logradouro TEXT,
            numero TEXT NOT NULL,
            complemento TEXT,
            bairro TEXT,
            cidade TEXT,
            senha TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    criar_tabela_usuarios()
    print("Banco de dados e tabela de usuários atualizados com sucesso para o modelo do front-end.")