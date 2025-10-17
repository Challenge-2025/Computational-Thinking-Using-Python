import sqlite3
import requests
import json
from database import conectar

class UsuarioManager:
    def __init__(self):
        pass

    def buscar_endereco_por_cep(self, cep):
        """Busca o endereço correspondente a um CEP usando a API ViaCEP e retorna os dados."""
        try:
            response = requests.get(f"https://viacep.com.br/ws/{cep.replace('-', '')}/json/")
            response.raise_for_status()
            dados_cep = response.json()
            if "erro" not in dados_cep:
                print("\n--- Endereço Encontrado via API ---")
                print(f"Logradouro: {dados_cep.get('logradouro', 'N/A')}")
                print(f"Bairro: {dados_cep.get('bairro', 'N/A')}")
                print(f"Cidade: {dados_cep.get('localidade', 'N/A')}")
                print("---------------------------------")
                return dados_cep
            else:
                print("\nCEP não encontrado.")
                return None
        except requests.exceptions.RequestException as e:
            print(f"\nErro ao consultar o CEP: {e}")
            return None

    def cadastrar(self, dados_usuario):
        '''Cadastra o usuário no banco de dados com base nos campos do front-end.'''
        
        endereco_api = self.buscar_endereco_por_cep(dados_usuario['cep'])
        if not endereco_api:
            print("Cadastro cancelado devido a CEP inválido.")
            return

        dados_usuario['logradouro'] = endereco_api.get('logradouro', '')
        dados_usuario['bairro'] = endereco_api.get('bairro', '')
        dados_usuario['cidade'] = endereco_api.get('localidade', '')

        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO usuarios (cpf, nome, email, telefone, nascimento, deficiencia, cep, logradouro, numero, complemento, bairro, cidade, senha)
                VALUES (:cpf, :nome, :email, :telefone, :nascimento, :deficiencia, :cep, :logradouro, :numero, :complemento, :bairro, :cidade, :senha)
            ''', dados_usuario)
            conn.commit()
            print(f"\nUsuário {dados_usuario['nome']} cadastrado com sucesso!")
        except sqlite3.IntegrityError as e:
            print(f"\nErro de integridade: {e}. O CPF ou E-mail já podem estar cadastrados.")
        except Exception as e:
            print(f"\nOcorreu um erro inesperado: {e}")
        finally:
            conn.close()

    def mostrarDados(self, cpf):
        """Mostra os dados do usuário a partir do banco de dados."""
        conn = conectar()
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM usuarios WHERE cpf = ?", (cpf,))
            usuario = cursor.fetchone()
            if usuario:
                print("\n--- Dados do Usuário ---")
                for key in usuario.keys():
                    if key != 'senha': # Não exibir a senha
                        print(f"{key.capitalize()}: {usuario[key]}")
                print("----------------------")
            else:
                print("\nUsuário não encontrado.")
        except Exception as e:
            print(f"\nOcorreu um erro inesperado: {e}")
        finally:
            conn.close()

    def alterarDados(self, cpf):
        """Altera dados do usuário no banco de dados."""
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM usuarios WHERE cpf = ?", (cpf,))
            if not cursor.fetchone():
                print("\nUsuário não encontrado.")
                return

            print("\n--- Alterar Dados Atuais do Usuário ---")
            print("1. Nome")
            print("2. CEP")
            print("3. Complemento")
            print("4. Senha")
            print("0. Cancelar")
            print("----------------------")
            opcao = input("Qual dado deseja alterar? ")
            print("----------------------")

            campo = None
            novo_valor = None

            if opcao == "1":
                campo = "nome"
                novo_valor = input("Digite o novo nome: ")
            elif opcao == "2":
                novo_cep = input("Digite o novo CEP: ")
                if self._buscar_endereco_por_cep(novo_cep):
                    campo = "cep"
                    novo_valor = novo_cep
                else:
                    print("Alteração cancelada, CEP inválido.")
                    return
            elif opcao == "3":
                campo = "complemento"
                novo_valor = input("Digite o novo complemento: ")
            elif opcao == "4":
                campo = "senha"
                novo_valor = input("Digite a nova senha: ").upper()
            elif opcao == "0":
                print("Alteração cancelada.")
                return
            else:
                print("Opção inválida.")
                return

            if campo and novo_valor is not None:
                cursor.execute(f"UPDATE usuarios SET {campo} = ? WHERE cpf = ?", (novo_valor, cpf))
                conn.commit()
                print("Dados atualizados com sucesso!")
        except Exception as e:
            print(f"\nOcorreu um erro inesperado: {e}")
        finally:
            conn.close()

    def apagarConta(self, cpf):
        """Deleta a conta do usuário do banco de dados."""
        confirmacao = input("Tem certeza que deseja deletar a conta? (s/n): ").lower()
        if confirmacao == "s":
            conn = conectar()
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM usuarios WHERE cpf = ?", (cpf,))
                conn.commit()
                if cursor.rowcount > 0:
                    print("Conta deletada com sucesso!")
                else:
                    print("\nUsuário não encontrado.")
            except Exception as e:
                print(f"\nOcorreu um erro inesperado: {e}")
            finally:
                conn.close()
        elif confirmacao == "n":
            print("Processo para deletar a conta cancelado!")
        else:
            print("Opção inválida, tente novamente.")

    def exportar_para_json(self, cpf):
        """Exporta os dados de um usuário para um arquivo JSON."""
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM usuarios WHERE cpf = ?", (cpf,))
            usuario_tuple = cursor.fetchone()

            if not usuario_tuple:
                print("\nUsuário não encontrado.")
                return

            usuario_dict = {
                "cpf": usuario_tuple[0],
                "nome": usuario_tuple[1],
                "cartao_sus": usuario_tuple[2],
                "cep": usuario_tuple[3],
                "complemento": usuario_tuple[4],
            }

            with open("dados_usuario.json", "w", encoding="utf-8") as json_file:
                json.dump(usuario_dict, json_file, indent=4, ensure_ascii=False)
            
            print(f"\nDados do usuário {usuario_dict['nome']} exportados com sucesso para 'dados_usuario.json'.")

        except Exception as e:
            print(f"\nOcorreu um erro inesperado ao exportar para JSON: {e}")
        finally:
            conn.close()

            

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

