import oracledb
import os

DB_USER = "RM562012"
DB_PASS = "070906"
DB_DSN = "oracle.fiap.com.br:1521/ORCL"

def conectar():
    """
    Conecta ao banco de dados Oracle e retorna um objeto de conexão.
    """
    try:
        conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
        print("\nConexão com o Oracle bem-sucedida!")
        return conn
    except oracledb.DatabaseError as e:
        print(f"\nERRO ao conectar ao Oracle: {e}")
        return None