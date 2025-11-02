# 🩺 Reabilita+ — Sistema de Gerenciamento de Pacientes (Sprint 4)

> Projeto desenvolvido para a disciplina de Pensamento Computacional com Python. O sistema evoluiu de um protótipo em SQLite para uma aplicação robusta conectada ao banco de dados Oracle, consumindo APIs externas (ViaCEP) e uma API de Inteligência Artificial interna (Flask/Scikit-learn).

## 👨‍💻 Autores

- Gabriel Bebé da Silva RM562012
- Pedro Ferreira Gomes RM565824

## 🚀 Funcionalidades da Sprint 4

- ✅ **Integração com Banco de Dados Oracle:**
  - Os dados dos pacientes são agora lidos e gravados diretamente no banco de dados corporativo da FIAP (Tabelas `T_RHSTU_PACIENTE` e `T_RHSTU_ENDERECO`).
  - Utiliza o módulo `oracledb` do Python para todas as operações.

- ✅ **CRUD Completo e Funcional (Multi-Tabela):**
  - **CREATE:** Cadastra um novo paciente e seu endereço em duas tabelas diferentes, tratando a transação.
  - **READ:** Consulta os dados de um paciente fazendo `JOIN` entre as tabelas de paciente e endereço.
  - **UPDATE:** Altera informações do paciente ou do endereço.
  - **DELETE:** Remove um paciente e **todos os seus dados relacionados** (endereços, consultas, lembretes, interações) na ordem correta para respeitar as Foreign Keys.

- ✅ **Consumo de API Externa (ViaCEP):**
  - Durante o cadastro (CREATE) e alteração (UPDATE), o sistema consulta a API do ViaCEP para validar o CEP e preencher automaticamente os campos de logradouro, bairro e cidade.

- ✅ **Consumo de API de Inteligência Artificial (Integração de Matérias):**
  - Nova funcionalidade no menu (Opção 8) que consome a API de IA (`app.py`, feita na matéria de AI & Chatbot) para prever a categoria de uma pergunta.

- ✅ **Exportação de Dados para JSON:**
  - Funcionalidade (Opção 6) que consulta os dados do paciente (com `JOIN`) e os exporta para um arquivo `.json` formatado.

- ✅ **Estrutura de Código Modular:**
  - `main.py`: Interface principal do usuário (menu de terminal).
  - `controller/usuario.py`: Classe `UsuarioManager` que encapsula toda a lógica de negócio e SQL.
  - `database.py`: Módulo dedicado à conexão com o banco de dados Oracle.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3
- **Banco de Dados:** Oracle (`oracledb`)
- **API Externa:** ViaCEP (`requests`)
- **API Interna (Consumida):** Flask (`requests`)
- **Manipulação de Dados:** `json`

## 🎥 Link para o Vídeo Explicativo (Sprint 4)

