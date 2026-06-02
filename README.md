# 📌 Smart Customer Support (Chatbot IA)

## 🤖 Système de support client intelligent basé sur Flask + Gemini API

Une application de chatbot intelligent qui automatise le support client grâce à l’intelligence artificielle (Google Gemini), avec historique des conversations, tableau de bord administrateur et base de données scalable.

---

# 🚀 Fonctionnalités

### 💬 Chat en temps réel
- Interface de chat interactive
- Historique des conversations par utilisateur
- Gestion de plusieurs conversations

### 🤖 Intelligence artificielle
- Propulsé par l’API Google Gemini
- Réponses contextuelles et intelligentes
- Compréhension du langage naturel

### 🧠 Gestion des conversations
- Stockage persistant des messages (MySQL)
- Organisation par conversation
- Suivi des messages utilisateur / bot

### 📊 Tableau de bord administrateur
- Consultation des conversations utilisateurs
- Suivi de l’activité du chatbot
- Statistiques de base (messages, utilisateurs, etc.)

### 🔐 Gestion des utilisateurs
- Authentification (login / inscription)
- Gestion des rôles (user / admin)

---

# 🏗️ Stack technique

- **Backend :** Flask (Python)
- **Base de données :** MySQL
- **ORM :** SQLAlchemy
- **IA :** Google Gemini API
- **Frontend :** HTML / CSS / JavaScript (ou React optionnel)
- **Authentification :** Flask-Login ou JWT

---

# 🗂️ Structure de la base de données

### 👤 Utilisateurs
- id
- username
- email
- password
- role

### 💬 Conversations
- id
- user_id
- title
- status
- created_at

### 🧾 Messages
- id
- conversation_id
- sender (user / bot)
- content
- timestamp

---

# ⚙️ Installation

## 1. Cloner le projet
```bash
git clone https://github.com/your-username/smart-customer-support.git
cd smart-customer-support
```

---

## 2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

---

## 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

---

## 4. Configurer les variables d’environnement
Créer un fichier `.env` :

```env
FLASK_APP=app.py
FLASK_ENV=development

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=chatbot_db

GEMINI_API_KEY=your_gemini_api_key
```

---

## 5. Initialiser la base de données
```bash
flask db init
flask db migrate -m "initialisation base de données"
flask db upgrade
```

---

## 6. Lancer le projet
```bash
flask run
```

---

# 💬 Fonctionnement

1. L’utilisateur envoie un message via le chat  
2. Le message est enregistré dans la base de données  
3. Le contexte est envoyé à Gemini API  
4. L’IA génère une réponse  
5. La réponse est sauvegardée et affichée  
6. L’historique complet est conservé  

---

# 📊 Exemple de conversation

Utilisateur : "Comment réinitialiser mon mot de passe ?"  
Bot : "Cliquez sur le lien mot de passe oublié..."  
Utilisateur : "Ça ne fonctionne pas"  
Bot : "Je vais vous guider étape par étape..."

---

# 🔥 Améliorations possibles

- Upload de fichiers (PDF, images)
- Mémoire IA avancée (RAG)
- Système de tickets support
- Interface mobile responsive
- Support multilingue
- Tableau de bord analytics avancé
- Transfert vers agent humain

---

# 🧠 Architecture

Interface utilisateur → API Flask → SQLAlchemy → MySQL → Gemini API

---

# 👨‍💻 Auteur

EZ wald

---

# 📜 Licence

Licence MIT
