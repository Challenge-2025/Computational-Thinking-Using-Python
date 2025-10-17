# 🩺 Reabilita+ — Sistema de Gerenciamento de Usuários da Saúde (Sprint 4)

> Projeto desenvolvido para a disciplina de Pensamento Computacional com Python. O sistema evoluiu de um protótipo em memória para uma aplicação robusta com persistência de dados em banco de dados, consumo de API externa e exportação de dados.

## 👨‍💻 Autores

- Gabriel Bebé da Silva RM562012
- Pedro Ferreira Gomes RM565824

## 🚀 Funcionalidades da Sprint 4

- ✅ **Integração com Banco de Dados SQLite:**
  - Os dados dos usuários são agora armazenados de forma persistente no arquivo `reabilita.db`.
  - Utiliza o módulo `sqlite3` do Python para todas as operações de banco de dados.

- ✅ **CRUD Completo e Funcional:**
  - **CREATE:** Cadastro de novos usuários no banco de dados.
  - **READ:** Consulta de dados de usuários existentes.
  - **UPDATE:** Alteração de informações como nome, CEP, complemento e senha.
  - **DELETE:** Remoção da conta do usuário do sistema.

- ✅ **Consumo de API Externa (ViaCEP):**
  - Durante o cadastro, o sistema consulta a API do ViaCEP para validar o CEP e exibir o endereço correspondente, melhorando a experiência do usuário.

- ✅ **Exportação de Dados para JSON:**
  - Nova funcionalidade no menu que permite ao usuário exportar seus dados (exceto a senha) para um arquivo `dados_usuario.json`.

- ✅ **Estrutura de Código Modular:**
  - `main.py`: Interface principal do usuário e fluxo do programa.
  - `controller/usuario.py`: Classe `UsuarioManager` que encapsula toda a lógica de negócio e interação com o banco.
  - `database.py`: Módulo dedicado à conexão e configuração inicial do banco de dados.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3
- **Banco de Dados:** SQLite 3
- **API Externa:** ViaCEP (`requests`)
- **Manipulação de Dados:** `json`

## 🔮 Próximos Passos

- Integração com o front-end desenvolvido em outras disciplinas.
- Desenvolvimento e/ou consumo de uma API REST para comunicação entre o back-end Python e o front-end.
- Validações de dados mais robustas (formato de CPF, força da senha, etc.).
- Implementação de testes automatizados.

## 🎥 Link para o Vídeo Explicativo (Sprint 4)

*Substitua pelo novo link do vídeo da Sprint 4*
https://youtu.be/kZMGAB4O1cM