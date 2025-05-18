# 🩺 Reabilita+ — Sistema de Cadastro e Login para Usuários da Saúde

> Projeto desenvolvido no contexto da disciplina de Computacional Thinking Using Python. Um sistema de terminal simples que permite o cadastro, login e gerenciamento de dados de usuários da área da saúde.

## 👨‍💻 Autores

- Bruno Andrade Zanateli RM563736
- Gabriel Bebé da Silva  RM562012
- Pedro Ferreira Gomes RM575824

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
- `usuario.py`: módulo com as funções reutilizáveis de cadastro, alteração, exclusão e exibição de dados.
- Estrutura pensada para ser reutilizável e extensível em sprints futuras.

## 🔮 Futuras Melhorias (Sprint futura)

- Integração com banco de dados
- Agendamento de consultas
- Validações mais robustas (ex: formato do CPF, campos obrigatórios)
- Testes automatizados
