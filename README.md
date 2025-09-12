# 🩺 Reabilita+ — Sistema de Cadastro e Login para Usuários da Saúde

> Projeto desenvolvido no contexto da disciplina de Pensamento Computacional com Python.Um sistema de terminal simples que permite o cadastro, login e gerenciamento de dados de usuários da área da saúde. Sistema orientado a objetos, com as operações de usuário encapsuladas em uma classe para maior organização e reutilização.

## 👨‍💻 Autores

- Gabriel Bebé da Silva  
- Pedro Ferreira Gomes

## 🚀 Funcionalidades

- ✅ Menu interativo com opções:
  - Login
  - Cadastro
  - Consulta de dados
  - Alteração de dados
  - Exclusão de conta
  - Ajuda
  - Sair
- ✅ Cadastro completo do usuário:
  - Nome completo
  - CPF
  - Cartão SUS
  - Endereço (CEP e complemento)
  - Senha
- ✅ Estrutura de dados organizada com dicionários
- ✅ Validações básicas:
  - CPF já cadastrado
  - Login com verificação de CPF e senha
- ✅ Menu de ajuda com opções simuladas (pronto para futuras funcionalidades)

## 🧠 Organização do Código

- `main.py`: contém a lógica principal do menu e navegação do sistema.
- `controller/usuario.py`: módulo com a classe `UsuarioManager`, responsável pelas operações de cadastro, alteração, exclusão, exibição de dados e menu de ajuda dos usuários.
- Estrutura pensada para ser reutilizável, organizada e extensível em sprints futuras.

## 🔮 Futuras Melhorias (Sprint futura)

- Integração com banco de dados
- Agendamento de consultas
- Validações mais robustas (ex: formato do CPF, campos obrigatórios)
- Testes automatizados
