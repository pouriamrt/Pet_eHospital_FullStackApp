# 🏥 Pet eHospital – Full Stack Application

A secure, AI-powered veterinary hospital platform enabling pet owners and doctors to manage pet health profiles, communicate in real-time, and facilitate online consultations. This platform uses Flask for the backend, WebSockets for live chat, Stripe for payments, and SQLite as the local database engine.

---

## 🔑 Key Features

### 👤 User Experience
- Secure signup & login (Flask-Login)
- Manage pet profiles with photo uploads
- Submit symptoms for AI-assisted diagnosis
- Real-time chat with doctors
- View consultation history
- Contact form with validation and confirmation

### 👨‍⚕️ Doctor Experience
- Doctor-specific authentication and dashboards
- Access to client and pet data
- Receive chat messages and payment history
- AI-generated suggestions based on pet conditions
- Maintain detailed medical records for pets

### 🤖 AI Suggestions
- AI module for preliminary diagnostic suggestions based on input symptoms
- Modular and extensible (`app/AI_suggestion/`)

### 💬 Real-Time Chat
- WebSocket-based real-time chat via Flask-SocketIO
- Event management (`app/chat/events.py`)
- Custom chat interface (`templates/chat.html`)
- Separate models for tracking messages and paid interactions

### 💳 Payment System
- Stripe integration for online consultations (`checkout/routes.py`)
- Success and cancel routes/templates
- Model for tracking paid consultations

---

## 🧱 Architecture & Structure

```bash
Pet_eHospital_FullStackApp/
├── app/
│   ├── auth/                # User & doctor authentication
│   ├── AI_suggestion/       # AI-powered health suggestion routes
│   ├── chat/                # WebSocket-based live chat logic
│   ├── checkout/            # Stripe payment integration
│   ├── doctor_main/         # Doctor dashboards and client views
│   ├── doctor_profile/      # Doctor profile update and views
│   ├── user_profile/        # User profile dashboard
│   ├── pet_profile/         # Manage pets, symptoms, and uploads
│   ├── models/              # SQLAlchemy models (Users, Pets, Chats, etc.)
│   ├── static/              # CSS, JS, Fonts, and Assets
│   └── templates/           # Jinja2 HTML templates
├── app.db                   # SQLite database
├── config.py                # App configuration (secret keys, DB URI)
├── extensions.py            # Flask extension bindings (db, login manager)
├── requirements.txt         # Dependencies
├── Dockerfile               # Container configuration
└── azure-pipelines.yml      # CI/CD workflow (Azure DevOps)
```

---

## 🧠 Tech Stack

| Layer         | Tech Used                                          |
|---------------|----------------------------------------------------|
| Backend       | Flask, Flask-SocketIO, SQLAlchemy, WTForms         |
| Frontend      | HTML5, CSS3, Bootstrap, jQuery                     |
| AI Engine     | Rule-based Flask Blueprint (`AI_suggestion`)       |
| Authentication| Flask-Login                                        |
| Database      | SQLite (can be swapped for PostgreSQL)             |
| Payments      | Stripe API Integration                             |
| Deployment    | Docker, PythonAnywhere, Azure Pipelines            |

---

## ⚙️ Getting Started

### 1. Clone & Navigate
```bash
git clone https://github.com/yourusername/Pet_eHospital_FullStackApp.git
cd Pet_eHospital_FullStackApp
```

### 2. Set Up Environment
```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run Locally
```bash
flask run
```

### 4. Optional Docker Deployment
```bash
docker build -t pet-ehospital .
docker run -p 5000:5000 pet-ehospital
```

---

## 🧪 Test Accounts

| Role   | Email                    | Password   |
|--------|--------------------------|------------|
| User   | test@pawspital.com       | 123456     |
| Doctor | dr.paws@pawspital.com    | docpass    |

---

## 📌 Developer Notes

- All models are defined in `app/models/` using SQLAlchemy.
- Chat events are handled in `chat/events.py` and consumed via Socket.IO.
- AI suggestions are modular, rule-based (can be enhanced with ML later).
- Paid chat history is stored and accessible under doctor/user profiles.
- The Stripe key should be stored securely using environment variables in production.
- Custom fonts and assets are under `static/`, ensuring rich UX.

---

## 🤝 Contributing

Pull requests are welcome! Feel free to open an issue to discuss new features or bugs.

---

## 📄 License

MIT License © 2025 Pouria Mortezaagha
