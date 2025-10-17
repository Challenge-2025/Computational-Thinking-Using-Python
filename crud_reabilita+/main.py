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
    print("\n ------- Seja Bem-vindo(a) ao Reabilita+ -------")
    while True:
        print("\n--- Menu Principal ---")
        print("1. Login")
        print("2. Cadastrar")
        print("3. Consultar meus dados")
        print("4. Alterar dados")
        print("5. Apagar conta")
        print("6. Exportar dados para JSON")
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
                cpf = input("Digite seu CPF: ")
                senhaC = input("Digite sua senha: ").upper()
                if login_valido(cpf, senhaC):
                    print("----------------------")
                    print("Login bem-sucedido!")
                    print("----------------------")
                else:
                    print("----------------------")
                    print("CPF ou senha incorretos.")
                    print("----------------------")

            case 2:
                nomeCompleto = input("Digite seu nome completo: ")
                cpf = input("Digite seu CPF: ")
                senhaR = input("Crie sua senha: ").upper()
                cartaoSus = input("Digite seu número do cartão SUS: ")
                cep = input("Digite seu CEP: ")
                complemento = input("Digite o complemento (ou deixe em branco): ")
                usuario_manager.cadastrar(nomeCompleto, cpf, cartaoSus, cep, complemento, senhaR)

            case 3:
                cpf = input("Digite seu CPF para consultar os dados: ")
                usuario_manager.mostrarDados(cpf)

            case 4:
                cpf = input("Digite seu CPF para alterar os dados: ")
                usuario_manager.alterarDados(cpf)

            case 5:
                cpf = input("Digite seu CPF para apagar a conta: ")
                usuario_manager.apagarConta(cpf)

            case 6:
                cpf = input("Digite seu CPF para exportar os dados: ")
                usuario_manager.exportar_para_json(cpf)
                
            case 7:
                # Simulando que o usuário precisa estar "logado" para pedir ajuda
                cpf = input("Digite seu CPF para acessar o menu de ajuda: ")
                usuario_manager.menuAjuda(cpf)

            case 0:
                print("Saindo do sistema...")
                print("----------------------")
                break

            case _:
                print("----------------------")
                print("Opção inválida. Tente novamente.")
                print("----------------------")

if __name__ == "__main__":
    menu()