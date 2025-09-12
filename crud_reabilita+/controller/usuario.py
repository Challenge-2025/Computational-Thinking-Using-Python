'''Uma clsse de usuarios realizando um armazenamento de funções com foco de conseguir ser mais organizado e reutilizavel'''

class UsuarioManager:
    def __init__(self):
        self.usuarios = {}

    def cadastrar(self,usuarios, nomeCompleto, cpf, cartaoSus, cep, complemento, senhaR):
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

    def mostrarDados(self,usuarios, cpf):
        """Mostra os dados do usuário no sistema"""
        try:
            dados = usuarios[cpf]  
            print("\n--- Dados do Usuário ---")
            print(f"Nome: {dados['dados_pessoais']['nome']}")
            print(f"CPF: {dados['dados_pessoais']['cpf']}")
            print(f"Cartão SUS: {dados['dados_pessoais']['cartao_sus']}")
            print(f"CEP: {dados['endereco']['cep']}")
            print(f"Complemento: {dados['endereco']['complemento']}")
            print("----------------------")
        except KeyError as e:
            print(f"\nErro: usuário ou campo '{e}' não encontrado.")
            print("----------------------")
        except Exception:
            print("\nOcorreu um erro inesperado ao tentar acessar os dados.")
            print("----------------------")


    def alterarDados(self,usuarios, cpf):
        """Alterar dados do usario dentro do sistema"""
        try:
            dados = usuarios[cpf]  
            print("\n--- Alterar Dados Atuais do Usuário ---")
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
        except KeyError as e:
            print(f"\nErro: usuário ou campo '{e}' não encontrado.")
            print("----------------------")
        except Exception:
            print("\nOcorreu um erro inesperado ao tentar alterar os dados.")
            print("----------------------")


    def apagarConta(self,usuarios, cpf):
        """Deleta a conta do usuário no sistema"""
        try:
            if cpf not in usuarios:
                print("\nUsuário não encontrado.")
                print("----------------------")
                return

            confirmacao = input("Tem certeza que deseja deletar a conta? (s/n): ").lower()
            print("----------------------")

            if confirmacao == "s":
                del usuarios[cpf]
                print("Conta deletada com sucesso!")
                print("----------------------")
            elif confirmacao == "n":
                print("Processo para deletar a conta cancelado!")
                print("----------------------")
            else:
                print("Opção inválida, tente novamente.")
                print("----------------------")

        except KeyError as e:
            print(f"\nErro: usuário ou campo '{e}' não encontrado.")
            print("----------------------")
        except Exception as e:
            print(f"\nOcorreu um erro inesperado: {e}")
            print("----------------------")


            

    def menuAjuda(self,usuarios, cpf):
        """Menu de ajuda com prováveis dúvidas do usuário"""
        try:
            if cpf not in usuarios:
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

            match opcao:
                case "1":
                    print("Você selecionou: Ver minha próxima consulta.")
                case "2":
                    print("Você selecionou: Alterar dados cadastrais.")
                case "3":
                    print("Você selecionou: Cancelar consulta.")
                case "4":
                    print("Você selecionou: Reagendar consulta.")
                case "5":
                    print("Você selecionou: Falar com atendente.")
                case "6":
                    print("Você selecionou: Saber localização da unidade.")
                case "7":
                    print("Você selecionou: Acessar laudos anteriores.")
                case "8":
                    print("Você selecionou: Instruções de acessibilidade.")
                case "9":
                    print("Você selecionou: Suporte técnico.")
                case "10":
                    print("Saindo do menu de ajuda.")
                case _:
                    print("Opção inválida. Por favor, escolha de 1 a 10.")
            print("----------------------")

        except KeyError as e:
            print(f"\nErro: usuário ou campo '{e}' não encontrado.")
            print("----------------------")
        except Exception as e:
            print(f"\nOcorreu um erro inesperado: {e}")
            print("----------------------")

