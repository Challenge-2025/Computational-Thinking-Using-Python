from controller.usuario import UsuarioManager
from database import criar_tabela_usuarios
import sqlite3

def login_valido(cpf, senha):
    """Verifica as credenciais do usuário no banco de dados."""
    conn = sqlite3.connect('reabilita.db')
    cursor = conn.cursor()
    cursor.execute("SELECT senha FROM usuarios WHERE cpf = ?", (cpf,))
    resultado = cursor.fetchone()
    conn.close()
    if resultado and resultado[0] == senha:
        return True
    return False

def menu():
    # Garante que a tabela exista ao iniciar o programa
    criar_tabela_usuarios()
    
    usuario_manager = UsuarioManager()
    print("\n ------- Seja Bem-vindo(a) ao Reabilita+ (Ferramenta de Gestão) -------")
    while True:
        print("\n--- Menu Principal ---")
        print("1. Login")
        print("2. Cadastrar Novo Usuário")
        print("3. Consultar Dados de Usuário")
        print("4. Alterar Dados de Usuário")
        print("5. Apagar Conta de Usuário")
        print("6. Exportar Dados para JSON")
        print("7. Ajuda")
        print("0. Sair")
        print("----------------------")

        try:
            opcao = int(input("Digite a opção desejada: "))
        except ValueError:
            print("Entrada inválida! Digite apenas números (0 a 7).")
            continue
        
        print("----------------------")

        match opcao:
            case 1:
                cpf = input("Digite o CPF do usuário: ")
                senhaC = input("Digite a senha: ").upper()
                if login_valido(cpf, senhaC):
                    print("\nLogin bem-sucedido!")
                else:
                    print("\nCPF ou senha incorretos.")

            case 2:
                print("--- Cadastro de Novo Usuário ---")
                dados_usuario = {
                    "nome": input("Nome completo: "),
                    "cpf": input("CPF: "),
                    "email": input("E-mail: "),
                    "telefone": input("Telefone: "),
                    "nascimento": input("Data de nascimento (AAAA-MM-DD): "),
                    "deficiencia": input("Possui deficiência? (SIM/NAO): "),
                    "cep": input("CEP: "),
                    "numero": input("Número da residência: "),
                    "complemento": input("Complemento (opcional): "),
                    "senha": input("Crie uma senha: ").upper()
                }
                usuario_manager.cadastrar(dados_usuario)

            case 3:
                cpf = input("Digite o CPF para consultar os dados: ")
                usuario_manager.mostrarDados(cpf)

            case 4:
                cpf = input("Digite o CPF do usuário a ser alterado: ")
                usuario_manager.alterarDados(cpf)

            case 5:
                cpf = input("Digite o CPF do usuário a ser apagado: ")
                usuario_manager.apagarConta(cpf)

            case 6:
                cpf = input("Digite o CPF para exportar os dados: ")
                usuario_manager.exportar_para_json(cpf)
                
            case 7:
                cpf = input("Digite seu CPF para acessar o menu de ajuda: ")
                usuario_manager.menuAjuda(cpf)

            case 0:
                print("Saindo do sistema...")
                break

            case _:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()