# DisSafe Shield API

![](https://img.shields.io/github/v/release/DebugCove/DisSafe-Shield-API?include_prereleases)  
![](https://img.shields.io/github/last-commit/DebugCove/DisSafe-Shield-API)  
![](https://img.shields.io/github/stars/DebugCove/DisSafe-Shield-API)  
![](https://img.shields.io/github/forks/DebugCove/DisSafe-Shield-API)  

The DisSafe Shield API is an API designed for a shared moderation bot, allowing multiple servers and communities to use a unified system to maintain order and security. The API acts as an intermediary between the database, the main API, and the bot, ensuring efficient and secure communication.  

## Features  

- **Shared Moderation**: Allows different communities to share blocklists, rules, and sanctions in an integrated way.  
- **Request Management**: Processes bot commands and provides quick responses based on stored moderation guidelines.  
- **Database Connection**: Keeps a secure record of infractions, permissions, and actions taken by the bot.  
- **Security and Authentication**: Uses robust authentication to ensure that only authorized users have access to administrative functions.  

## Tech Stack  

- **Language**: Python (Django)  
- **Database**: MySQL  
- **Authentication**: Bearer  
- **Communication Protocols**: RESTful  

## Installation  

1. Clone the repository:  

   ```bash
   git clone https://github.com/DebugCove/DisSafe-Shield-API
   cd DisSafe-Shield-API
   ```  

2. Install the dependencies:  

   ```bash
   pip install -r requirements.txt
   ```  

3. Configure the environment variables:  

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

4. Run the application:  

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```  

## Usage  

The API provides endpoints for moderation, blocklists, and server management. The interactive documentation can be accessed at:  

```bash
http://IP_DJANGO/docs
```  

or  

```bash
http://IP_DJANGO/api/
```  

## Contributing  

Fork the repository  

Create a branch with your feature:  

```bash
git checkout -b my-feature
```  

Commit your changes:  

```bash
git commit -m ‘Add new feature’
```  

Push to the repository:  

```bash
git push origin my-feature
```  

Open a Pull Request  

## License  

This project is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Public License](LICENSE.md) – see the LICENSE file for more details.
