# 🧠 Career Growth Agent

The **Career Growth Agent** is an intelligent, consent-based recommendation system built using FastAPI and React. It enables users to:

* **Upload professional profiles** (LinkedIn `.zip`, Resume `.pdf`, GitHub username)
* **Parse and extract skills & experience**
* **Analyze skill gaps** against a job role by fetching real job descriptions
* **Receive personalized job recommendations** from external APIs (e.g., Adzuna)
* All actions are protected via a **token-based consent mechanism**

The agent integrates various NLP, scraping, and parsing techniques to extract meaningful career data and support proactive, skill-oriented job recommendations.

---

## 🚀 Features

- 🔍 Extract skills/experience from LinkedIn, GitHub, and Resume
- 🧠 Analyze job descriptions and compare against user skills
- 📊 Recommend jobs from public APIs (e.g., Adzuna)
- 🔐 Built-in consent and token validation system for each action
- ⚙️ Modular agents for parsing and analyzing

---

## 🛠️ Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/career-growth-agent.git
cd career-growth-agent
```

### 2. Set Up Backend

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run FastAPI Backend

```bash
uvicorn main:app --reload
```

This will start the API server at `http://127.0.0.1:8000`

### 4. Frontend Setup (React + Vite)

```bash
cd ui
npm install
npm run dev
```

UI runs at `http://localhost:5173` by default

---

## ⚙️ API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/upload_linkedin/` | POST | Upload and parse LinkedIn archive (`.zip`) |
| `/resume/` | POST | Upload and parse Resume (`.pdf`) |
| `/parse_github/` | POST | Analyze GitHub profile for tech skills |
| `/analyze_skill_gap/` | POST | Compare your skills with job requirements |
| `/recommend_jobs/` | POST | Get personalized job recommendations |

⚠️ **Note:** Consent tokens are issued on uploads and validated internally by agents.

---

## 🧪 Sample Usage Flow

1. **Enter User ID**
2. **Upload either:**
   * LinkedIn archive
   * Resume
   * GitHub username
3. **Analyze a job title** for skill gap
4. **Receive recommended jobs** that match your profile

---

## 📁 Project Structure

```
career-growth-agent/
├── hushh_mcp/
│   └── agents/
│       └── career_growth_agent/
│           ├── career.py
│           ├── linkedin.py
│           ├── resume.py
│           ├── github.py
│           ├── skills_gap.py
│           ├── job_fetcher.py
│           └── job_recommender.py
├── ui/
│   ├── components/
│   │   ├── UploadResume.jsx
│   │   ├── UploadLinkedIn.jsx
│   │   ├── ParseGithub.jsx
│   │   ├── AnalyzeSkillGap.jsx
│   │   └── RecommendJobs.jsx
│   ├── App.jsx
│   ├── main.jsx
│   └── App.css
├── main.py
├── requirements.txt
├── vite.config.js
└── README.md
```

---

## 🔐 Consent Handling

* Tokens are **issued** on file uploads and stored internally
* Tokens are **validated** inside agents (e.g., `CareerGrowthAgent`, `SkillAnalyzerAgent`)
* The UI does **not need to send tokens**; they are auto-managed by backend agents

---

## 🚀 Technology Stack

- **Backend:** FastAPI, Python, NLP Libraries
- **Frontend:** React, Vite, JavaScript
- **APIs:** Adzuna Jobs API, GitHub API
- **Security:** Token-based consent validation
- **Architecture:** Modular agent-based system

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Maintainer

**Aman Singh**
- 📧 Email: `amansingh@example.com`
- 💼 LinkedIn: [linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile)

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📚 Documentation

For detailed API documentation, visit `http://127.0.0.1:8000/docs` when running the FastAPI server.

---

## ⭐ Show your support

Give a ⭐️ if this project helped you!