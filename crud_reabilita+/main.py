from controller.usuario import UsuarioManager
from database import conectar
import oracledb

def login_valido(cpf, senha):
    """Verifica as credenciais do paciente no banco de dados Oracle."""
    conn = conectar()
    if not conn:
        return False
    
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT SENHA FROM T_RHSTU_PACIENTE 
            WHERE NR_CPF = :cpf
            """, {'cpf': cpf})
        
        resultado = cursor.fetchone()
        
        if resultado and resultado[0] == senha:
            return True
        return False
    except oracledb.DatabaseError as e:
        print(f"Erro no login: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def menu():

    usuario_manager = UsuarioManager()
    print("\n ------- Seja Bem-vindo(a) ao Reabilita+ (Gestão de Pacientes - Oracle) -------")
    
    while True:
        print("\n--- Menu Principal ---")
        print("1. Login")
        print("2. Cadastrar Novo Paciente")
        print("3. Consultar Dados do Paciente")
        print("4. Alterar Dados do Paciente")
        print("5. Apagar Conta do Paciente")
        print("6. Exportar Dados (JSON)")
        print("7. Ajuda (Simples)")
        print("8. Testar API do Chatbot (IA)")
        print("0. Sair")
        print("----------------------")

        try:
            opcao = int(input("Digite a opção desejada: "))
        except ValueError:
            print("Entrada inválida! Digite apenas números (0 a 8).")
            continue
        
        print("----------------------")

        match opcao:
            case 1:
                cpf = input("Digite o CPF do paciente: ")
                senhaC = input("Digite a senha: ")
                if login_valido(cpf, senhaC):
                    print("\nLogin bem-sucedido!")
                else:
                    print("\nCPF ou senha incorretos.")

            case 2:
                print("--- Cadastro de Novo Paciente ---")
                dados_usuario = {
                    # Tabela PACIENTE
                    "nome": input("Nome completo: "),
                    "cpf": input("CPF (11 dígitos): "),
                    "email": input("E-mail: "),
                    "telefone": input("Telefone (ex: 11988887777): "),
                    "nascimento": input("Data de nascimento (ex: 10/01/2000): "),
                    "deficiencia": input("Possui deficiência? (SIM/NAO): "),
                    "senha": input("Crie uma senha: "),
                    
                    # Tabela ENDERECO
                    "cep": input("CEP (ex: 01001000): "),
                    "numero": input("Número da residência: "),
                    "complemento": input("Complemento (opcional, aperte ENTER para pular): ")
                }

                if not all([dados_usuario['nome'], dados_usuario['cpf'], dados_usuario['email'], dados_usuario['senha'], dados_usuario['cep'], dados_usuario['numero']]):
                    print("\nCampos obrigatórios (Nome, CPF, Email, Senha, CEP, Numero) não podem ficar em branco.")
                else:
                    usuario_manager.cadastrar(dados_usuario)

            case 3:
                cpf = input("Digite o CPF para consultar os dados: ")
                usuario_manager.mostrarDados(cpf)

            case 4:
                cpf = input("Digite o CPF do paciente a ser alterado: ")
                usuario_manager.alterarDados(cpf)

            case 5:
                cpf = input("Digite o CPF do paciente a ser apagado: ")
                usuario_manager.apagarConta(cpf)

            case 6:
                cpf = input("Digite o CPF para exportar os dados: ")
                usuario_manager.exportar_para_json(cpf)
                
            case 7:
                usuario_manager.menuAjuda(None, None) 

            case 8:
                usuario_manager.chamar_chatbot_ia()

            case 0:
                print("Saindo do sistema...")
                break

            case _:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()