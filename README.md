# DisSafe Shield API
[![Bandit Security Analysis](https://github.com/DebugCove/DisSafe-Shield-API/actions/workflows/bandit.yml/badge.svg)](https://github.com/DebugCove/DisSafe-Shield-API/actions/workflows/bandit.yml)
![](https://img.shields.io/github/v/release/DebugCove/DisSafe-Shield-API?include_prereleases)
![](https://img.shields.io/github/last-commit/DebugCove/DisSafe-Shield-API)

![](https://img.shields.io/github/stars/DebugCove/DisSafe-Shield-API)
![](https://img.shields.io/github/forks/DebugCove/DisSafe-Shield-API)

The Dissafe Shield API is an API designed for a shared moderation bot, allowing multiple servers and communities to use a unified system to maintain order and security. The API acts as an intermediary between the database, the main API and the bot, ensuring efficient and secure communication.
## Features

- Shared moderation: Allows different communities to share blocklists, rules and sanctions in an integrated way.
- Request Management: Processes bot commands and provides quick responses based on stored moderation guidelines.
- Database Connection: Keeps a secure record of infractions, permissions and actions taken by the bot.
- Security and Authentication: Uses robust authentication to ensure that only authorised users have access to administrative functions.


## Stack used

- Language: Python (Django) 
- Database: MySQL
- Authentication: Bearer
- Communication protocols: RESTful 


## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/DebugCove/DisSafe-Shield-API
   cd DisSafe-Shield-API
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure as variáveis de ambiente:
   ```env
    HOST=
    PORT=
    SECRET_KEY=
    DB_HOST=
    DB_USER=
    DB_PASS=
    DB_DTB=
    DB_DTB_TESTING=
    DB_PORT=
   ```
4. Execute a aplicação:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```


## Usage

The API provides endpoints for moderation, block lists and server management. The interactive documentation can be accessed at:
```bash
http://IP_DJANGO/docs
```


## Contributing

Fork the repository

Create a branch with your functionality:

```bash
git checkout -b my-functionality
```

Commit your changes:

```bash
git commit -m ‘Add new feature’
```

Commit to the repository:

```bash
git push origin my-feature
```

Open a Pull Request


## License

This project is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Public License](LICENSE.md)  Licence - see the LICENSE file for more details.


