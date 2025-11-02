import oracledb
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
                print("\n--- Endereço Encontrado via API (ViaCEP) ---")
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

    def _usuario_existe(self, cpf):
        """Verifica se um paciente existe no banco de dados Oracle."""
        conn = conectar()
        if not conn:
            return False
        
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT NR_CPF FROM T_RHSTU_PACIENTE WHERE NR_CPF = :cpf", {'cpf': cpf})
            resultado = cursor.fetchone()
            return resultado is not None
        except oracledb.DatabaseError as e:
            print(f"Erro ao verificar usuário: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def cadastrar(self, dados_usuario):
        '''Cadastra o paciente e seu endereço no banco Oracle.'''

        endereco_api = self.buscar_endereco_por_cep(dados_usuario['cep'])
        if not endereco_api:
            print("Cadastro cancelado devido a CEP inválido.")
            return

        conn = conectar()
        if not conn:
            print("Cadastro cancelado. Não foi possível conectar ao banco.")
            return
        
        cursor = conn.cursor()
        
        try:
            id_paciente_var = cursor.var(int)

            sql_paciente = """
                INSERT INTO T_RHSTU_PACIENTE (
                    NM_COMPLETO, NR_CPF, DT_NASCIMENTO, DS_EMAIL, 
                    SENHA, NR_TELEFONE, FL_POSSUI_DEFICIENCIA
                ) VALUES (
                    :nome, :cpf, :nascimento, :email, 
                    :senha, :telefone, :deficiencia
                )
                RETURNING ID_PACIENTE INTO :id_paciente_var
            """
            dados_paciente = {
                'nome': dados_usuario['nome'],
                'cpf': dados_usuario['cpf'],
                'nascimento': dados_usuario['nascimento'],
                'email': dados_usuario['email'],
                'senha': dados_usuario['senha'],
                'telefone': dados_usuario['telefone'],
                'deficiencia': dados_usuario['deficiencia'].upper(),
                'id_paciente_var': id_paciente_var
            }
            cursor.execute(sql_paciente, dados_paciente)
            
            id_paciente_gerado = id_paciente_var.getvalue()[0]
            print(f"Paciente inserido com ID: {id_paciente_gerado}")

            sql_endereco = """
                INSERT INTO T_RHSTU_ENDERECO (
                    NM_LOGRADOURO, NR_NUMERO, NM_COMPLEMENTO, NM_BAIRRO,
                    NM_CIDADE, NR_CEP, ID_PACIENTE
                ) VALUES (
                    :logradouro, :numero, :complemento, :bairro,
                    :cidade, :cep, :id_paciente
                )
            """

            dados_endereco = {
                'logradouro': endereco_api.get('logradouro', ''),
                'numero': dados_usuario['numero'],
                'complemento': dados_usuario.get('complemento', ''),
                'bairro': endereco_api.get('bairro', ''),
                'cidade': endereco_api.get('localidade', ''),
                'cep': dados_usuario['cep'].replace('-', ''),
                'id_paciente': id_paciente_gerado 
            }
            cursor.execute(sql_endereco, dados_endereco)

            conn.commit()
            print(f"\nPaciente {dados_usuario['nome']} e seu endereço foram cadastrados com sucesso!")

        except oracledb.IntegrityError as e:
            conn.rollback()
            print(f"\nErro de integridade: {e}. O CPF ou E-mail já podem estar cadastrados.")
        except oracledb.DatabaseError as e:
            conn.rollback()
            print(f"\nOcorreu um erro de banco de dados: {e}")
        except Exception as e:
            conn.rollback()
            print(f"\nOcorreu um erro inesperado: {e}")
        finally:
            cursor.close()
            conn.close()

    def mostrarDados(self, cpf):
        """Mostra os dados do paciente e seu endereço (JOIN)."""
        conn = conectar()
        if not conn:
            return
        
        cursor = conn.cursor()
        try:
            sql_join = """
                SELECT 
                    P.NM_COMPLETO, P.NR_CPF, P.DS_EMAIL, P.NR_TELEFONE, 
                    P.DT_NASCIMENTO, P.FL_POSSUI_DEFICIENCIA,
                    E.NM_LOGRADOURO, E.NR_NUMERO, E.NM_COMPLEMENTO, 
                    E.NM_BAIRRO, E.NM_CIDADE, E.NR_CEP
                FROM 
                    T_RHSTU_PACIENTE P
                JOIN 
                    T_RHSTU_ENDERECO E ON P.ID_PACIENTE = E.ID_PACIENTE
                WHERE 
                    P.NR_CPF = :cpf
            """
            cursor.execute(sql_join, {'cpf': cpf})
            
            # Pega os nomes das colunas
            colunas = [d[0] for d in cursor.description]
            paciente = cursor.fetchone()

            if paciente:
                print("\n--- Dados do Paciente ---")
                dados_paciente = dict(zip(colunas, paciente))
                for key, value in dados_paciente.items():
                    print(f"{key.replace('_', ' ').capitalize()}: {value}")
                print("----------------------")
            else:
                print("\nPaciente não encontrado.")
        except oracledb.DatabaseError as e:
            print(f"\nErro ao consultar dados: {e}")
        finally:
            cursor.close()
            conn.close()

    def alterarDados(self, cpf):
        """Altera dados do paciente ou endereço."""
        if not self._usuario_existe(cpf):
            print("\nPaciente não encontrado.")
            return

        print("\n--- Qual dado deseja alterar? ---")
        opcoes = {
            "1": ("PACIENTE", "NM_COMPLETO"), 
            "2": ("PACIENTE", "DS_EMAIL"), 
            "3": ("PACIENTE", "NR_TELEFONE"), 
            "4": ("ENDERECO", "NR_CEP"),
            "5": ("ENDERECO", "NR_NUMERO"), 
            "6": ("ENDERECO", "NM_COMPLEMENTO"), 
            "7": ("PACIENTE", "SENHA")
        }
        for key, (_, col) in opcoes.items():
            print(f"{key}. {col.replace('_', ' ').capitalize()}")
        print("0. Cancelar")
        print("----------------------")
        
        opcao = input("Digite a opção: ")
        if opcao == "0":
            print("Alteração cancelada.")
            return
        if opcao not in opcoes:
            print("Opção inválida.")
            return

        tabela, campo = opcoes[opcao]
        
        if campo == 'NR_CEP':
            print("--- Alteração de Endereço (CEP) ---")
            novo_cep = input("Digite o novo CEP: ")
            endereco = self.buscar_endereco_por_cep(novo_cep)
            if not endereco:
                print("Alteração cancelada, CEP inválido.")
                return
            
            sql_update = """
                UPDATE T_RHSTU_ENDERECO SET 
                    NM_LOGRADOURO = :log, 
                    NM_BAIRRO = :bairro, 
                    NM_CIDADE = :cidade,
                    NR_CEP = :cep
                WHERE ID_PACIENTE = (SELECT ID_PACIENTE FROM T_RHSTU_PACIENTE WHERE NR_CPF = :cpf)
            """
            params = {
                'log': endereco.get('logradouro', ''),
                'bairro': endereco.get('bairro', ''),
                'cidade': endereco.get('localidade', ''),
                'cep': novo_cep.replace('-', ''),
                'cpf': cpf
            }
        else:
            novo_valor = input(f"Digite o novo valor para {campo.replace('_', ' ').capitalize()}: ")
            
            tabela_sql = f"T_RHSTU_{tabela}"
            
            if tabela == "PACIENTE":
                sql_update = f"UPDATE {tabela_sql} SET {campo} = :valor WHERE NR_CPF = :cpf"
            else:
                sql_update = f"""
                    UPDATE {tabela_sql} SET {campo} = :valor 
                    WHERE ID_PACIENTE = (SELECT ID_PACIENTE FROM T_RHSTU_PACIENTE WHERE NR_CPF = :cpf)
                """
            params = {'valor': novo_valor, 'cpf': cpf}

        conn = conectar()
        if not conn:
            return
        cursor = conn.cursor()
        try:
            cursor.execute(sql_update, params)
            conn.commit()
            print("\nDados atualizados com sucesso!")
        except oracledb.DatabaseError as e:
            conn.rollback()
            print(f"\nErro ao atualizar dados: {e}")
        finally:
            cursor.close()
            conn.close()

    def apagarConta(self, cpf):
        """Deleta o paciente e seu endereço."""
        if not self._usuario_existe(cpf):
            print("\nPaciente não encontrado.")
            return

        confirmacao = input(f"Tem certeza que deseja deletar o paciente com CPF {cpf}? (s/n): ").lower()
        if confirmacao != "s":
            print("\nOperação cancelada.")
            return

        conn = conectar()
        if not conn:
            return
        cursor = conn.cursor()
        
        # Delatar na ordem inversa dop shcema, para não ocorrer erro foregein key
        # 1. LEMBRETE -> 2. CONSULTA -> 3. INTERACAO -> 4. ENDERECO -> 5. PACIENTE
        
        try:
            # Pega o ID do Paciente
            cursor.execute("SELECT ID_PACIENTE FROM T_RHSTU_PACIENTE WHERE NR_CPF = :cpf", {'cpf': cpf})
            id_paciente = cursor.fetchone()[0]

            sql_del_lembrete = """
                DELETE FROM T_RHSTU_LEMBRETE_CONSULTA 
                WHERE ID_CONSULTA IN (SELECT ID_CONSULTA FROM T_RHSTU_CONSULTA WHERE ID_PACIENTE = :id)
            """
            cursor.execute(sql_del_lembrete, {'id': id_paciente})

            cursor.execute("DELETE FROM T_RHSTU_CONSULTA WHERE ID_PACIENTE = :id", {'id': id_paciente})
            
            cursor.execute("DELETE FROM T_RHSTU_INTERACAO_CHATBOT WHERE ID_PACIENTE = :id", {'id': id_paciente})

            cursor.execute("DELETE FROM T_RHSTU_ENDERECO WHERE ID_PACIENTE = :id", {'id': id_paciente})

            cursor.execute("DELETE FROM T_RHSTU_PACIENTE WHERE ID_PACIENTE = :id", {'id': id_paciente})

            conn.commit()
            print(f"\nPaciente (CPF: {cpf}) e todos os seus dados associados (endereço, consultas, etc.) foram deletados com sucesso!")

        except oracledb.DatabaseError as e:
            conn.rollback()
            print(f"\nErro ao deletar conta: {e}")
        except Exception as e:
            conn.rollback()
            print(f"\nOcorreu um erro inesperado: {e}")
        finally:
            cursor.close()
            conn.close()

    def exportar_para_json(self, cpf):
        """Exporta os dados (JOIN) de um paciente para um arquivo JSON."""
        conn = conectar()
        if not conn:
            return
        
        cursor = conn.cursor()
        try:
            sql_join = """
                SELECT 
                    P.NM_COMPLETO, P.NR_CPF, P.DS_EMAIL, P.NR_TELEFONE, 
                    P.DT_NASCIMENTO, P.FL_POSSUI_DEFICIENCIA,
                    E.NM_LOGRADOURO, E.NR_NUMERO, E.NM_COMPLEMENTO, 
                    E.NM_BAIRRO, E.NM_CIDADE, E.NR_CEP
                FROM 
                    T_RHSTU_PACIENTE P
                JOIN 
                    T_RHSTU_ENDERECO E ON P.ID_PACIENTE = E.ID_PACIENTE
                WHERE 
                    P.NR_CPF = :cpf
            """
            cursor.execute(sql_join, {'cpf': cpf})
            colunas = [d[0] for d in cursor.description]
            paciente = cursor.fetchone()

            if not paciente:
                print("\nPaciente não encontrado.")
                return
            
            usuario_dict = dict(zip(colunas, paciente))
            nome_arquivo = f"dados_paciente_{cpf}.json"

            with open(nome_arquivo, "w", encoding="utf-8") as json_file:
                json.dump(usuario_dict, json_file, indent=4, ensure_ascii=False)
            
            print(f"\nDados do paciente {usuario_dict['NM_COMPLETO']} exportados com sucesso para '{nome_arquivo}'.")

        except oracledb.DatabaseError as e:
            print(f"\nErro ao exportar dados: {e}")
        except Exception as e:
            print(f"\nOcorreu um erro inesperado ao exportar para JSON: {e}")
        finally:
            cursor.close()
            conn.close()

    def menuAjuda(self,usuarios, cpf):
        """Menu de ajuda"""
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