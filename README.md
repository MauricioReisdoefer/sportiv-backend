# Sportiv Backend

Este repositório contém o código-fonte do backend para o aplicativo Sportiv, uma plataforma dedicada à criação e gerenciamento de torneios esportivos. Desenvolvido em Python, este backend segue uma arquitetura MVC (Model-View-Controller) e é responsável por gerenciar dados de usuários, torneios e outras funcionalidades essenciais do aplicativo.

## Funcionalidades

- **Gerenciamento de Usuários:** Criação, autenticação e gerenciamento de perfis de usuário.
- **Autenticação JWT:** Implementação de JSON Web Tokens para segurança e autenticação de APIs.
- **Estrutura MVC:** Organização clara do código em Models, Views (controladores) e Controllers para facilitar a manutenção e escalabilidade.
- **Testes:** Inclui testes para controladores e modelos, garantindo a robustez e confiabilidade do sistema.

## Tecnologias Utilizadas

- **Python:** Linguagem de programação principal.
- **Flask:** Baseado na estrutura de arquivos e commits, é provável que utilize Flask para o desenvolvimento web.
- **SQLAlchemy:** Para interação com o banco de dados, dada a presença de modelos.
- **Pytest:** Para execução dos testes.
- **JWT:** Para autenticação segura.
- **Werkzeug:** Para criar senhas hash.

## Configuração do Ambiente

Para configurar o ambiente de desenvolvimento e executar o projeto localmente, siga os passos abaixo:

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/MauricioReisdoefer/sportiv-backend.git
    cd sportiv-backend
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # No Linux/macOS
    # venv\Scripts\activate  # No Windows
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuração do Banco de Dados:**
    ..

## Como Executar

Após configurar o ambiente, você pode executar o servidor backend:

```bash
python main.py
```

O servidor estará disponível em `http://localhost:5000` (porta padrão do Flask, pode variar).

## Testes

Para executar os testes do projeto, utilize o Pytest:

```bash
python -m pytest
```

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Estrutura do Projeto

O projeto `sportiv-backend` segue uma estrutura MVC (Model-View-Controller) para organizar o código de forma modular e escalável:

```
sportiv-backend/
├── controllers/        # Lógica de negócio e manipulação de requisições
│   ├── __init__.py
│   └── user_controller.py
├── models/             # Definição dos modelos de dados e interação com o banco de dados
│   ├── __init__.py
│   └── user_model.py
├── routes/             # Definição das rotas da API
│   ├── __init__.py
│   └── user_routes.py
├── test/               # Testes unitários e de integração
│   ├── __init__.py
│   ├── models/
│   └── controllers/
├── util/               # Utilitários e funções auxiliares
│   ├── __init__.py
│   ├── auth.py
│   └── db.py
├── .gitignore          # Arquivos e diretórios a serem ignorados pelo Git
├── LICENSE             # Licença do projeto
├── main.py             # Ponto de entrada da aplicação
└── requirements.txt    # Dependências do projeto
```

## Endpoints da API (Exemplos)

Null

## Contribuição

Contribuições são bem-vindas! Se você deseja contribuir para o projeto Sportiv Backend, siga estas diretrizes:

1.  Faça um fork do repositório.
2.  Crie uma nova branch para sua feature (`git checkout -b feature/sua-feature`).
3.  Faça suas alterações e escreva testes quando aplicável.
4.  Certifique-se de que todos os testes passem.
5.  Faça commit de suas alterações (`git commit -m \'FEAT: Adiciona nova funcionalidade\'`).
6.  Envie para a branch (`git push origin feature/sua-feature`).
7.  Abra um Pull Request detalhando suas alterações.

## Suporte

Para dúvidas ou problemas, por favor, abra uma [issue](https://github.com/MauricioReisdoefer/sportiv-backend/issues) neste repositório.
