# GPT_ClONE

# 💬 Flask ChatGPT 3.5 Web App

A simple and interactive chatbot interface built using **Flask**, **Bootstrap**, and the **OpenAI GPT-3.5 API**. Users can register, chat with GPT, and view their chat history via a responsive web UI.

---

## 🚀 Features

- 🧠 Chat with GPT-3.5 via OpenAI API
- 🔐 User authentication (Register/Login/Logout)
- 📝 Persistent chat history (searchable)
- 👤 Profile page with update option
- 🖼️ Beautiful responsive UI using Bootstrap
- 💾 SQLite database integration

---

## 📂 Project Structure

├── app.py # Main Flask app
├── gpt.py # OpenAI GPT interaction logic
├── templates/ # HTML Jinja2 templates
├── static/ # CSS, images, JavaScript
├── instance/ # Config or instance folder (e.g., database)
├── database.db # SQLite database file
├── requirements.txt # Python dependencies
├── README.md # This file

yaml
Copy
Edit

---

## ⚙️ Setup Instructions

### 1. Clone the repository


git clone https://github.com/your-username/flask-chatgpt-ui.git
cd flask-chatgpt-ui

### 2. Install dependencies

```pip install -r requirements.txt```

### 3. Set your OpenAI API Key
Create a .env file or use environment variables:

```OPENAI_API_KEY=your_openai_api_key_here```

### 4. Run the Flask app

```python app.py```
```Access the app at: http://127.0.0.1:5000```

🔐 Authentication
Register with your email and password

Login to start chatting

Chats are saved per user session

📸 Screenshots
You can add screenshots of:

Login/Register UI
<img width="1919" height="1078" alt="Screenshot 2025-07-16 164203" src="https://github.com/user-attachments/assets/b14ff7d7-fd3c-4fee-81a5-943e703f5807" />
<img width="1919" height="1079" alt="Screenshot 2025-07-16 164251" src="https://github.com/user-attachments/assets/56c54828-5376-4075-8cf0-200fcb933ea2" />

Chat Interface
<img width="1919" height="1079" alt="Screenshot 2025-07-16 164339" src="https://github.com/user-attachments/assets/9615fd3f-4ca8-4092-8d1e-cc00702b523b" />

Chat History
<img width="1919" height="1079" alt="Screenshot 2025-07-16 164412" src="https://github.com/user-attachments/assets/e75d7fe3-489c-4a51-b261-c50fb73821c2" />

Profile Page
<img width="1919" height="1079" alt="Screenshot 2025-07-16 164433" src="https://github.com/user-attachments/assets/e0f2a620-d353-4a1e-a788-2d1b5c43c802" />

🧠 Powered By
Flask

Bootstrap

OpenAI GPT-3.5 API

SQLite

📄 License
MIT License. Feel free to use and modify!

✨ Author
Developed by [Kunjan Patel]
[[Your Email or GitHub Profile Link](https://github.com/Kunjan1112)]

---

### ✅ Tips:
- Add a `.env.example` to show others how to set their environment variable.
- Add screenshots to show the UI if you upload to GitHub.
- Add instructions for deploying (e.g., Render, Heroku, Docker) if relevant.
