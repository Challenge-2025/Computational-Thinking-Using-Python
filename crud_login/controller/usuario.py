def cadastrar(usuarios, nomeCompleto, cpf, cartaoSus, cep, complemento, senhaR):
    usuarios[cpf] = {
        "dados_pessoais": {
            "nome": nomeCompleto,
            "cpf": cpf,
            "cartao_sus": cartaoSus
        },
        "endereco": {
            "cep": cep,
            "complemento": complemento
        },
        "acesso": {
            "senha": senhaR
        }
    }
    
    print(f"\nUsuário {nomeCompleto}cadastrado com sucesso!")
    print(f"CPF: {cpf}")
    print(f"Cartão SUS: {cartaoSus}")
    print(f"CEP: {cep}")
    print(f"Complemento: {complemento}")

def mostrardados(usuarios, cpf):
    if cpf in usuarios:
        print("\n--- Dados do Usuário ---")
        print(f"Nome: {usuarios[cpf]['dados_pessoais']['nome']}")
        print(f"CPF: {usuarios[cpf]['dados_pessoais']['cpf']}")
        print(f"Cartão SUS: {usuarios[cpf]['dados_pessoais']['cartao_sus']}")
        print(f"CEP: {usuarios[cpf]['endereco']['cep']}")
        print(f"Complemento: {usuarios[cpf]['endereco']['complemento']}")
        print("----------------------")
    else:
        print("\nUsuário não encontrado.")
        print("----------------------")

def alterardados(usuarios, cpf):
    if cpf not in usuarios:
        print("\nUsuário não encontrado.")
        print("----------------------")
        return

    print("\n--- Alterar Dados ---")
    print("1. Nome")
    print("2. CEP")
    print("3. Complemento")
    print("4. Senha")
    print("0. Cancelar")

    print("----------------------")
    opcao = input("Qual dado deseja alterar? ")
    print("----------------------")

    if opcao == "1":
        novo_nome = input("Digite o novo nome: ")
        usuarios[cpf]["dados_pessoais"]["nome"] = novo_nome
    elif opcao == "2":
        novo_cep = input("Digite o novo CEP: ")
        usuarios[cpf]["endereco"]["cep"] = novo_cep
    elif opcao == "3":
        novo_complemento = input("Digite o novo complemento: ")
        usuarios[cpf]["endereco"]["complemento"] = novo_complemento
    elif opcao == "4":
        nova_senha = input("Digite a nova senha: ")
        usuarios[cpf]["acesso"]["senha"] = nova_senha
    elif opcao == "0":
        print("Alteração cancelada.")
        print("----------------------")
        return
    else:
        print("Opção inválida.")
        print("----------------------")
        return

    print("Dados atualizados com sucesso!")
    print("----------------------")

def apagarconta(usuarios, cpf):
    if cpf not in usuarios:
        print("\nUsuário não encontrado.")
        return
    
    confirmacao = input("\nTem certeza que deseja apagar seus dados?")
    if confirmacao == "s": 
        del usuarios[cpf]
        print("Conta deletada com sucesso!")
        print("----------------------")
    elif confirmacao == "n":
        print("Processo para deletar a conta cancelado!")
        print("----------------------")
    else:
        print("Opção invalida, tente novamente")
        return   