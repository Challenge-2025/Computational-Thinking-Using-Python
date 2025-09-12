from controller.usuario import UsuarioManager


def menu():
    usuarios = {}
    usario_manager = UsuarioManager()
    print("\n ------- Seja Bem-vindo(a) ao Reabilita+ -------")
    while True:
        print("1. Login")
        print("2. Cadastrar")
        print("3. Confirmar dados")
        print("4. Alterar dados")
        print("5. Apagar conta")
        print("6. Dúvidas")
        print("0. Sair")
        print("----------------------")

        try:
            opcao = int(input("Digite a opção desejada: "))
        except ValueError:
            print("Entrada inválida! Digite apenas números (0 a 6).")
            print("----------------------")
            continue
        except EOFError:
            print("\nEntrada finalizada inesperadamente. Saindo...")
            break

        print("----------------------")

        if (opcao == 3 and not usuarios):
            print("Não foi possível acessar seus dados. Efetue o cadastro primeiro!")
        else:
            match opcao:
                case 1:
                    cpf = input("Digite seu CPF: ")
                    senhaC = input("Digite sua senha: ").upper()
                    try:
                        if usuarios[cpf]["acesso"]["senha"] == senhaC:
                            print("----------------------")
                            print("Login bem-sucedido!")
                            print("----------------------")
                        else:
                            print("----------------------")
                            print("Senha incorreta.")
                            print("----------------------")
                    except KeyError:
                        print("----------------------")
                        print("CPF não encontrado. Por favor, cadastre-se primeiro.")
                        print("----------------------")

                case 2:
                    nomeCompleto = input("Digite seu nome completo: ")
                    cpf = input("Digite seu CPF: ")
                    senhaR = input("Digite sua senha: ").upper()
                    cartaoSus = input("Digite seu número do cartão SUS: ")
                    cep = input("Digite seu CEP: ")
                    complemento = input("Digite seu complemento: ")
                    usario_manager.cadastrar(usuarios, nomeCompleto, cpf, cartaoSus, cep, complemento, senhaR)

                case 3:
                    cpf = input("Digite seu CPF para consultar os dados: ")
                    usario_manager.mostrarDados(usuarios, cpf)

                case 4:
                    cpf = input("Digite seu CPF: ")
                    usario_manager.alterarDados(usuarios, cpf)

                case 5:
                    cpf = input("Digite seu CPF: ")
                    usario_manager.apagarConta(usuarios, cpf)

                case 6:
                    cpf = input("Digite seu CPF: ")
                    usario_manager.menuAjuda(usuarios, cpf)

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
