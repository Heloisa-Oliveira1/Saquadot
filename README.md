# 🐾 SaquaDot — Adoção Responsável em Saquarema  

> Um sistema web desenvolvido para facilitar o processo de **adoção responsável de animais**, conectando cuidadores e adotantes de forma simples, segura e intuitiva.

---

## 📋 Sumário  
1. [Visão Geral](#visão-geral-)  
2. [Principais Funcionalidades](#principais-funcionalidades-)  
3. [Tecnologias Utilizadas](#tecnologias-utilizadas-)  
4. [Instalação e Configuração](#instalação-e-configuração-)    
5. [Estrutura do Projeto](#estrutura-do-projeto-)  
6. [Futuras Implementações](#futuras-implementações-)

---

<a id="visão-geral-"></a>
## 💡 Visão Geral  

O **SaquaDot** é um aplicativo web criado para promover a adoção responsável de cães e gatos na cidade de **Saquarema – RJ**.  
Seu objetivo é conectar cuidadores de animais com pessoas interessadas em adotar, garantindo transparência, cuidado e segurança no processo.  

Desenvolvido com **Django (Python)** e **Bootstrap**, o sistema conta com um design simples, responsivo e intuitivo, além de funcionalidades como sistema de login, notificações, e painel de gerenciamento para cuidadores e adotantes.

---

<a id="principais-funcionalidades-"></a>
## ✨ Principais Funcionalidades  

### 🧑‍💻 Usuário (Adotante)
- Criar conta e fazer login.  
- Visualizar animais disponíveis para adoção.  
- Filtrar animais por espécie (cachorro/gato) e idade.  
- Solicitar adoção de um animal.  
- Acompanhar o status de suas solicitações.  
- Receber notificações sobre o andamento dos pedidos.  

### 🐕 Cuidador
- Cadastrar novos animais (com foto, descrição e contato).  
- Gerenciar seus próprios cadastros.  
- Aprovar ou recusar solicitações de adoção.  
- Receber notificações automáticas sobre novos pedidos.  

**OBS:** Atualmente não há uma distinção entre contas de Adotante e Cuidador. Um pode fazer o que o outro faz.

### 🔔 Sistema de Notificações
- Exibe notificações em tempo real.  
- Opção de marcar notificações como lidas ou apagar histórico.  
- Contador de notificações não lidas na barra de navegação.  

### 💬 Interface Amigável
- Design moderno com **Bootstrap 5** e ícones personalizados.  
- Efeitos visuais suaves em cards, botões e mensagens.  
- Feedbacks visuais ao copiar informações, realizar ações ou enviar formulários.  

---

<a id="tecnologias-utilizadas-"></a>
## 🛠️ Tecnologias Utilizadas  

| Categoria | Tecnologias |
|------------|--------------|
| **Back-end** | Python 3.x, Django 5 |
| **Front-end** | HTML5, CSS3, JavaScript, Bootstrap 5 |
| **Banco de Dados** | SQLite (padrão do Django) |
| **Controle de Versão** | Git e GitHub |
| **Ferramentas** | Visual Studio Code, Figma (protótipo), Git Bash |

---

<a id="instalação-e-configuração-"></a>
## ⚙️ Instalação e Configuração  

### 🔧 Pré-requisitos  
Certifique-se de ter instalado:  
- [Python 3.x](https://www.python.org/downloads/)  
- [Git](https://git-scm.com/)  
- [pip](https://pip.pypa.io/en/stable/)

---

### 📦 Passos para executar o projeto localmente  

```bash
# 1. Clonar o repositório
git clone https://github.com/Heloisa-Oliveira1/Saquadot.git
cd saquadot

# 2. Criar e ativar o ambiente virtual
python -m venv .venv
.\.venv\Scripts\activate  # Windows

# 3. Instalar as dependências
pip install django
python -m pip install Pillow

# 4. Criar um superusuário (opcional)
python manage.py createsuperuser

# 5. Executar o servidor local
python manage.py runserver
```

**Acesse:** http://127.0.0.1:8000/

---

<a id="estrutura-do-projeto-"></a>
## 📁 Estrutura do Projeto  

```
SaquaDot/
│
├── core/                     # Aplicação principal (animais, adoções, notificações etc.)
│   ├── migrations/            # Migrações do banco de dados
│   ├── templates/             # Templates HTML do app 'core'
│   ├── static/                # Arquivos estáticos (CSS, JS, imagens)
│   ├── admin.py               # Registro de modelos no painel admin
│   ├── apps.py                # Configurações do app
│   ├── models.py              # Modelos de dados (Animal, Adoção, Notificação, etc.)
│   ├── urls.py                # Rotas específicas do app
│   ├── views.py               # Lógica das páginas e requisições
│   └── forms.py               # Formulários Django usados nas views
│
├── media/                    # Imagens enviadas pelos usuários (fotos dos animais)
│
├── saquadot/                 # Pasta de configuração principal do projeto
│   ├── __init__.py
│   ├── asgi.py                # Configuração ASGI (para deploys assíncronos)
│   ├── settings.py            # Configurações gerais (apps, banco de dados, mídia, etc.)
│   ├── urls.py                # Mapeamento das rotas globais
│   └── wsgi.py                # Configuração WSGI (para servidores web)
│
├── users/                    # Aplicação responsável por cadastro e autenticação de usuários
│   ├── templates/             # Templates relacionados ao login, registro e perfil
│   ├── admin.py
│   ├── models.py              # Modelos relacionados ao usuário (perfil, etc.)
│   ├── forms.py               # Formulários de registro e login
│   ├── urls.py
│   └── views.py
│
├── db.sqlite3                # Banco de dados local SQLite
│
├── manage.py                 # Script principal do Django (migrações, servidor, etc.)
│
└── README.md                 # Documentação do projeto (descrição, instalação, uso)
```

---

<a id="futuras-implementações-"></a>
## 🚀 Futuras Implementações  

- [ ] Chat entre cuidador e adotante.  
- [ ] Sistema de campanhas para ONGs (atualmente só o admin pode cadastrar campanhas).  
- [ ] Filtros avançados (porte, raça, localização).  
- [ ] Upload múltiplo de fotos por animal.  

---

## 💚 Desenvolvido por  

**Equipe SaquaDot** — com amor e dedicação aos animais de Saquarema. 🐶🐱  
💻 Projeto acadêmico desenvolvido em Python/Django.
