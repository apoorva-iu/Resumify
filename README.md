<img width="1517" height="861" alt="image" src="https://github.com/user-attachments/assets/519ac8c5-8fe1-479d-badc-737543f344c8" /># 🚀 Resumify AI - Career Development Platform

A modern, React-style Streamlit application that helps users analyze their resumes, identify skill gaps, and access curated learning resources to boost their careers.

![Resumify AI](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.51.0-red)
![License](https://img.shields.io/badge/License-MIT-green)


## 📸 Project Preview
> 🚀 A quick look at the Resumify platform in action:

### 🏠 Homepage
<img width="1600" height="639" alt="image" src="https://github.com/user-attachments/assets/56e487ec-10e5-41c6-ae16-a31d41925f25" />

### Sign UP
<img width="1094" height="857" alt="image" src="https://github.com/user-attachments/assets/b3d702f9-aaeb-45b2-b9b5-955b4f9c067c" />

### Login 

### 📊 Dashboard
<img width="1600" height="725" alt="image" src="https://github.com/user-attachments/assets/2e9406e6-4b46-411d-b8a7-f6b4d7ec3032" />


### 💼 Resume Analysis
<img width="1600" height="702" alt="image" src="https://github.com/user-attachments/assets/d7c9090a-2119-4ce5-b094-e14fb2ca2d9e" />

<img width="1600" height="712" alt="image" src="https://github.com/user-attachments/assets/a51d76bc-dbc4-4f76-8099-170da57fc028" />


### 📚 Skill Hub
<img width="1517" height="861" alt="image" src="https://github.com/user-attachments/assets/dfd61d0f-d1ae-43bc-ac7a-f145d6ea52f2" />


### 💡 Job Recommendation
<img width="1600" height="732" alt="image" src="https://github.com/user-attachments/assets/9bf078ae-59d1-4619-8471-7fce1a481e98" />


### 🤖 AI Chatbot
<img width="1600" height="726" alt="image" src="https://github.com/user-attachments/assets/02afc851-7011-4f32-982f-d8aebae09f5f" />


### 🎤 Mock Interview
<img width="1600" height="652" alt="image" src="https://github.com/user-attachments/assets/a637d487-0f36-4b75-bfa5-91c914d0d062" />

<img width="1600" height="689" alt="image" src="https://github.com/user-attachments/assets/a348a272-e89d-4439-9752-5ce5ad98caa7" />

<img width="1600" height="599" alt="image" src="https://github.com/user-attachments/assets/11f1058c-7590-4bbd-879c-01b47d038b60" />


## ✨ Features

### 🔐 **Authentication System**
- Secure user registration and login
- Password hashing with SHA-256
- Session management
- User-specific data isolation

### 💼 **Resume Analyzer**
- Upload resumes in PDF or DOCX format
- AI-powered skill extraction
- Match analysis against target job roles
- Visual skill gap analysis with charts
- Personalized recommendations

### 🤖 **AI Chatbot**
- Powered by Groq's LLaMA 3 model
- User-specific chat history
- Real-time message storage in database
- Career guidance and skill development advice
- Beautiful chat interface with message bubbles

### ⚡ **Skill Hub**
- Curated learning resources for 30+ skills
- YouTube video tutorials with thumbnails
- Interactive resource cards
- Role-based skill recommendations
- Progress tracking

### 🎨 **Modern UI/UX**
- React-inspired design with Streamlit
- Gradient backgrounds and smooth animations
- Card-based layouts with hover effects
- Responsive design
- Interactive sidebar navigation
- Beautiful color schemes

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for API calls and resources)

## 🚀 Quick Start

### 1. Clone or Download the Project

```bash
# If using Git
git clone <repository-url>
cd pro

# Or download and extract the ZIP file
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env

# Or create manually
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edit `.env` and add your Groq API key:

```env
GROQ_API_KEY=your_actual_groq_api_key_here
```

**Get your FREE Groq API key:**
1. Visit [https://console.groq.com/keys](https://console.groq.com/keys)
2. Sign up or log in
3. Create a new API key
4. Copy and paste it into your `.env` file

### 4. Run the Application

```bash
streamlit run app.py
```

The application will open automatically in your default browser at `http://localhost:8501`

## 📁 Project Structure

```
pro/
├── app.py                      # Main application entry point
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .env                       # Your environment variables (create this)
├── README.md                  # This file
│
├── auth/                      # Authentication module
│   ├── __init__.py
│   ├── login.py              # Login page
│   └── signup.py             # Signup page
│
├── pages/                     # Application pages
│   ├── __init__.py
│   ├── chatbot.py            # AI chatbot interface
│   ├── upload_analyze.py    # Resume analyzer
│   └── skill_hub.py          # Learning resources
│
├── utils/                     # Utility functions
│   ├── __init__.py
│   └── database.py           # Database operations
│
└── data/                      # Database storage (created automatically)
    └── user.db               # SQLite database
```

## 🎯 Supported Job Roles

The application supports skill analysis for the following roles:

1. **Software Engineer** - Python, Java, C++, Git, Algorithms, Data Structures, SQL
2. **Data Analyst** - Python, SQL, R, Excel, Statistics, Tableau, PowerBI
3. **Frontend Developer** - HTML, CSS, JavaScript, React, Git, UI/UX, TypeScript
4. **Backend Developer** - Python, Java, Node.js, SQL, APIs, Docker, Git
5. **Machine Learning Engineer** - Python, ML, TensorFlow, PyTorch, Data Structures, SQL
6. **DevOps Engineer** - Linux, Docker, Kubernetes, AWS, CI/CD, Git, Python
7. **Cybersecurity Analyst** - Cybersecurity, Networking, Linux, Python, Ethical Hacking

## 📚 How to Use

### Step 1: Create an Account
1. Click on "✨ New user? Create Account"
2. Enter your username, email, and password
3. Click "🎉 Create Account"

### Step 2: Log In
1. Enter your email and password
2. Click "🚀 Login"

### Step 3: Upload & Analyze Resume
1. Navigate to "💼 Upload & Analyze" from the sidebar
2. Select your target job role
3. Upload your resume (PDF or DOCX)
4. View your skill match score and analysis
5. Identify skills you have and skills to learn

### Step 4: Explore Learning Resources
1. Navigate to "⚡ Skill Hub" from the sidebar
2. Browse curated YouTube tutorials for each skill
3. Click on video thumbnails to start learning
4. Track your progress as you acquire new skills

### Step 5: Get AI Career Guidance
1. Navigate to "🤖 AI Chatbot" from the sidebar
2. Ask questions about career development
3. Get personalized recommendations
4. Your chat history is automatically saved

## 🔧 Configuration

### Database Configuration

The application uses SQLite for data storage. The database is automatically created at `data/user.db` when you first run the app.

**Database Tables:**

1. **users** - Stores user accounts
   - id (PRIMARY KEY)
   - username (UNIQUE)
   - email (UNIQUE)
   - password (hashed)

2. **user_chats** - Stores chat history
   - id (PRIMARY KEY)
   - user_id (FOREIGN KEY)
   - sender (user/bot)
   - message
   - timestamp

### API Configuration

The chatbot uses Groq's API for AI responses. Make sure to set your API key in the `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

## 🎨 UI Customization

The application uses custom CSS for styling. You can modify the appearance by editing the `st.markdown()` CSS sections in:

- `app.py` - Global styles and sidebar
- `auth/login.py` - Login page styles
- `auth/signup.py` - Signup page styles
- `pages/chatbot.py` - Chat interface styles
- `pages/upload_analyze.py` - Upload page styles
- `pages/skill_hub.py` - Skill hub styles

## 🔒 Security Features

- **Password Hashing**: All passwords are hashed using SHA-256
- **Session Management**: Secure session state management
- **User Isolation**: Each user can only access their own data
- **Input Validation**: Form inputs are validated before processing
- **SQL Injection Prevention**: Parameterized queries prevent SQL injection

## 🐛 Troubleshooting

### Issue: "Module not found" error

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "API key not found" error

**Solution:**
1. Make sure you created a `.env` file (not just `.env.example`)
2. Verify your Groq API key is correct
3. Ensure there are no extra spaces in the `.env` file

### Issue: Database errors

**Solution:**
1. Delete the `data/user.db` file
2. Restart the application
3. The database will be recreated automatically

### Issue: Port already in use

**Solution:**
```bash
# Run on a different port
streamlit run app.py --server.port 8502
```

### Issue: Resume not being analyzed

**Solution:**
1. Ensure your resume is in PDF or DOCX format
2. Check that the file size is under 200MB
3. Try converting your resume to a different format

## 📊 Performance Tips

- **Large Resumes**: If analyzing large resumes, allow a few seconds for processing
- **Chat History**: Clear chat history periodically for better performance
- **Multiple Users**: The app supports concurrent users with isolated data

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Future Enhancements

- [ ] Support for more file formats (TXT, RTF)
- [ ] Advanced analytics dashboard
- [ ] Email notifications for skill progress
- [ ] Integration with job boards
- [ ] Resume builder
- [ ] Interview preparation module
- [ ] Skill assessment tests
- [ ] Career roadmap generator
- [ ] Export reports as PDF
- [ ] Multi-language support

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Streamlit** - For the amazing web framework
- **Groq** - For providing free AI API access
- **YouTube** - For hosting free educational content
- **Community Contributors** - For curated learning resources

## 📧 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review the [How to Use](#-how-to-use) guide
3. Create an issue on GitHub (if available)

## 🌟 Star History

If you find this project helpful, please consider giving it a star! ⭐

---

**Made with ❤️ using Streamlit and Python**

*Happy Learning! 🚀*
