import sqlite3
import requests
import json
from database import conectar

class UsuarioManager:
    def __init__(self):
        pass

    def _usuario_existe(self, cpf):
        """Verifica se um usuário existe no banco de dados."""
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT cpf FROM usuarios WHERE cpf = ?", (cpf,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado is not None

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
                    if key != 'senha':
                        print(f"{key.replace('_', ' ').capitalize()}: {usuario[key]}")
                print("----------------------")
            else:
                print("\nUsuário não encontrado.")
        except Exception as e:
            print(f"\nOcorreu um erro inesperado: {e}")
        finally:
            conn.close()

    def alterarDados(self, cpf):
        """Altera dados do usuário no banco de dados."""
        if not self._usuario_existe(cpf):
            print("\nUsuário não encontrado.")
            return

        print("\n--- Qual dado deseja alterar? ---")
        opcoes = {
            "1": "nome", "2": "email", "3": "telefone", "4": "cep", 
            "5": "numero", "6": "complemento", "7": "senha"
        }
        for key, value in opcoes.items():
            print(f"{key}. {value.capitalize()}")
        print("0. Cancelar")
        print("----------------------")
        
        opcao = input("Digite a opção: ")
        if opcao == "0":
            print("Alteração cancelada.")
            return
        if opcao not in opcoes:
            print("Opção inválida.")
            return

        campo = opcoes[opcao]
        novo_valor = input(f"Digite o novo valor para {campo}: ")
        
        conn = conectar()
        cursor = conn.cursor()
        try:
            if campo == 'cep':
                endereco = self.buscar_endereco_por_cep(novo_valor)
                if not endereco:
                    print("Alteração cancelada, CEP inválido.")
                    return
                cursor.execute("UPDATE usuarios SET logradouro = ?, bairro = ?, cidade = ? WHERE cpf = ?", 
                               (endereco.get('logradouro', ''), endereco.get('bairro', ''), endereco.get('localidade', ''), cpf))

            cursor.execute(f"UPDATE usuarios SET {campo} = ? WHERE cpf = ?", (novo_valor.upper() if campo == 'senha' else novo_valor, cpf))
            conn.commit()
            print("\nDados atualizados com sucesso!")
        except Exception as e:
            print(f"\nOcorreu um erro inesperado: {e}")
        finally:
            conn.close()

    def apagarConta(self, cpf):
        """Deleta a conta do usuário do banco de dados."""
        if not self._usuario_existe(cpf):
            print("\nUsuário não encontrado.")
            return

        confirmacao = input("Tem certeza que deseja deletar a conta? (s/n): ").lower()
        if confirmacao == "s":
            conn = conectar()
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM usuarios WHERE cpf = ?", (cpf,))
                conn.commit()
                print("\nConta deletada com sucesso!")
            except Exception as e:
                print(f"\nOcorreu um erro inesperado: {e}")
            finally:
                conn.close()
        else:
            print("\nOperação cancelada.")

    def exportar_para_json(self, cpf):
        """Exporta os dados de um usuário para um arquivo JSON."""
        conn = conectar()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM usuarios WHERE cpf = ?", (cpf,))
            usuario = cursor.fetchone()
            if not usuario:
                print("\nUsuário não encontrado.")
                return

            # Converte o objeto Row em um dicionário e remove a senha
            usuario_dict = dict(usuario)
            del usuario_dict['senha']

            with open(f"dados_{cpf}.json", "w", encoding="utf-8") as json_file:
                json.dump(usuario_dict, json_file, indent=4, ensure_ascii=False)
            
            print(f"\nDados do usuário {usuario_dict['nome']} exportados com sucesso para 'dados_{cpf}.json'.")
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


    def chamar_chatbot_ia(self):
        """
        Chama a API de AI & Chatbot (app.py) que está rodando localmente
        para classificar a intenção de uma pergunta.
        """
        print("\n--- Teste da API de IA (Chatbot) ---")
        print("A API app.py deve estar rodando em http://127.0.0.1:5000")
        
        pergunta = input("Digite uma pergunta (ex: 'como agendo?'): ")
        
        if not pergunta:
            print("Nenhuma pergunta inserida. Operação cancelada.")
            return

        try:
            dados_json = {"pergunta": pergunta}
            
            response = requests.post("http://127.0.0.1:5000/prever_categoria", json=dados_json)
            
            response.raise_for_status()
                     
            resposta_json = response.json()
            
            print("\n--- Resposta da API de IA ---")
            print(f"Pergunta Enviada: '{pergunta}'")
            print(f"Categoria Prevista: '{resposta_json.get('categoria_prevista', 'N/A')}'")
            print("-----------------------------")

        except requests.exceptions.ConnectionError:
            print("\nERRO: Não foi possível conectar à API de IA.")
            print("Verifique se o script 'app.py' está em execução no outro terminal.")
        except Exception as e:
            print(f"\nOcorreu um erro inesperado ao chamar a API: {e}")