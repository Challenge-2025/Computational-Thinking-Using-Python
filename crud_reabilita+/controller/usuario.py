'''Armazenamento de funçõe com foco de conseguir ser mais organizado e reutilizavel'''

def cadastrar(usuarios, nomeCompleto, cpf, cartaoSus, cep, complemento, senhaR):
    '''Cadastra o usário ao sistema'''
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
    
    print(f"\nUsuário {nomeCompleto} cadastrado com sucesso!")
    print(f"CPF: {cpf}")
    print(f"Cartão SUS: {cartaoSus}")
    print(f"CEP: {cep}")
    print(f"Complemento: {complemento}")
    print("----------------------")

def mostrarDados(usuarios, cpf):
    """Mostra os dados do usario no sistema"""
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

def alterarDados(usuarios, cpf):
    """Alterar dados do usario dentro do sistema"""
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

def apagarConta(usuarios, cpf):
    """Deleta a conta do usario no sistema"""
    if cpf not in usuarios:
        print("\nUsuário não encontrado.")
        print("----------------------")
        return
    
    confirmacao = input("\nTem certeza que deseja apagar seus dados?")
    print("----------------------")
    if confirmacao == "s": 
        del usuarios[cpf]
        print("Conta deletada com sucesso!")
        print("----------------------")
    elif confirmacao == "n":
        print("Processo para deletar a conta cancelado!")
        print("----------------------")
    else:
        print("Opção invalida, tente novamente")
        print("----------------------")
        return   
    

def menuAjuda(usarios, cpf):
    """Menu de ajuda com provaveis duvidsas que o usario pode ter"""
    if cpf not in usarios:
            print("\nUsuário não encontrado.")
            print("----------------------")
            return

    print("\n--- Menu Ajuda ---")
    print("1 - Ver minha próxima consulta")
    print("2 - Alterar dados cadastrais")
    print("3 - Cancelar consulta")
    print("4 - Reagendar consulta")
    print("5 - Falar com atendente")
    print("6 - Saber localização da unidade")
    print("7 - Acessar laudos anteriores")
    print("8 - Instruções de acessibilidade")
    print("9 - Suporte técnico")
    print("10 - Sair da ajuda")

    print("----------------------")
    opcao = input("Escolha uma opção (1 a 10): ")
    print("----------------------")

    '''OBS: Essa funções de ajuda abaixo atualmente nao executam nada por ser necessário dados externos que iremos
    conseguir executa-los apartir da proxima spritn :)'''

    match opcao:
        case "1":
            print("Você selecionou: Ver minha próxima consulta.")
            print("----------------------")
        case "2":
            print("Você selecionou: Alterar dados cadastrais.")
            print("----------------------")
        case "3":
            print("Você selecionou: Cancelar consulta.")
            print("----------------------")
        case "4":
            print("Você selecionou: Reagendar consulta.")
            print("----------------------")
        case "5":
            print("Você selecionou: Falar com atendente.")
            print("----------------------")
        case "6":
            print("Você selecionou: Saber localização da unidade.")
            print("----------------------")
        case "7":
            print("Você selecionou: Acessar laudos anteriores.")
            print("----------------------")
        case "8":
            print("Você selecionou: Instruções de acessibilidade.")
            print("----------------------")
        case "9":
            print("Você selecionou: Suporte técnico.")
            print("----------------------")
        case "10":
            print("Saindo do menu de ajuda.")
            print("----------------------")
        case _:
            print("Opção inválida. Por favor, escolha de 1 a 10.")
            print("----------------------")
