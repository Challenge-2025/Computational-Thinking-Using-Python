from controller.usuario import cadastrar, mostrarDados, alterarDados, apagarConta, menuAjuda

def menu():
    usuarios = {}
    print("\n ------- Seja Bem-vindo(a) ao Reabilita+ -------")
    while True:
        
        print("1. Login")
        print("2. Cadastrar")
        print("3. Confirmar dados")
        print("4. Alterar dados")
        print("5. Apagar conta")
        print("6. Duvidas")
        print("0. Sair")
        
        print("----------------------")
        opcao = int(input("Digite a opção desejada: "))
        print("----------------------")

        if (opcao == 3 and not usuarios):
            print("Não foi possível acessar seus dados. Efetue o cadastro primeiro!")
        else:

            
            match opcao:
                case 1:
                    cpf = input("Digite seu CPF: ")
                    senhaC = input("Digite sua senha: ")

                    if cpf not in usuarios:
                        print("\nCPF não encontrado. Por favor, cadastre-se primeiro.")
                    elif usuarios[cpf]["senha"] == senhaC:
                        print("\nLogin bem-sucedido!")
                    else:
                        print("\nSenha incorreta.")

                case 2:
                    nomeCompleto = input("Digite seu nome completo: ")
                    cpf = input("Digite seu CPF: ")
                    senhaR = input("Digite sua senha: ")
                    cartaoSus = input("Digite seu número do cartão SUS: ")
                    cep = input("Digite seu CEP: ")
                    complemento = input("Digite seu complemento: ")

                    cadastrar(usuarios, nomeCompleto, cpf, cartaoSus, cep, complemento, senhaR)

                case 3:
                    cpf = input("Digite seu CPF para consultar os dados:" )
                    mostrarDados(usuarios, cpf)

                case 4:
                    cpf = input("Digite seu CPF: ")
                    alterarDados(usuarios, cpf)

                case 5:
                    cpf = input("Digite seu CPF: ")
                    apagarConta(usuarios, cpf)

                case 6:
                    cpf = input("Digite seu CPF: ")
                    menuAjuda(usuarios, cpf)

                case 0:
                    print("\nSaindo do sistema...")
                    break

                case _:
                    print("\nOpção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
