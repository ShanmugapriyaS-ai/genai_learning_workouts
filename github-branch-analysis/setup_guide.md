# 🚀 Quick Setup Guide

## 5-Minute Setup for GitHub Branch Analysis Dashboard

---

## Step 1: Prerequisites Check ✅

Before starting, ensure you have:
- [ ] Python 3.8 or higher installed
- [ ] pip installed
- [ ] Internet connection
- [ ] GitHub account

**Check Python version:**
```bash
python --version
# Should show: Python 3.8.x or higher
```

---

## Step 2: Get GitHub Personal Access Token 🔑

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. Give it a name: `Branch Analysis Dashboard`
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
5. Click **"Generate token"**
6. **COPY THE TOKEN** (you won't see it again!)

---

## Step 3: Download Project Files 📥

```bash
# Clone the repository
git clone https://github.com/yourusername/github-branch-analysis.git

# Navigate to project directory
cd github-branch-analysis
```

**OR download ZIP from GitHub and extract it**

---

## Step 4: Install Dependencies 📦

```bash
# Install all required packages
pip install -r requirements.txt
```

**Wait for installation to complete** (may take 2-3 minutes)

---

## Step 5: Configure GitHub Token 🔧

1. Open `input_flask_enhanced_v2.py` in a text editor
2. Find line 9:
   ```python
   GITHUB_TOKEN = 'github_pat_11B4JOCKA0DtTL1EBV8jd5_...'
   ```
3. Replace with your token:
   ```python
   GITHUB_TOKEN = 'your_token_here'
   ```
4. Save the file

⚠️ **IMPORTANT:** Do NOT commit this file with your token to GitHub!

---

## Step 6: Start the Application 🎮

### Terminal 1 - Flask API

```bash
python input_flask_enhanced_v2.py
```

**Expected output:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

✅ **Leave this terminal running!**

### Terminal 2 - Streamlit Dashboard

Open a **NEW terminal** in the same directory:

```bash
streamlit run streamlit_dashboard_v3.py
```

**Expected output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
```

✅ **Browser should open automatically!**

---

## Step 7: Test the Dashboard 🧪

1. In the browser, you should see the dashboard
2. Enter test repository:
   - **GitHub Owner:** `kubernetes`
   - **Repository Name:** `kubernetes`
3. Click **"🚀 Fetch & Analyze Repository"**
4. Watch the progress bar (takes 30-60 seconds)
5. Explore all visualizations!

---

## Common Issues & Quick Fixes 🔧

### Issue: "ModuleNotFoundError"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Connection refused" or "Failed to fetch data"
**Solution:** Make sure Flask is running in Terminal 1

### Issue: "401 Unauthorized"
**Solution:** Check your GitHub token is correct and has `repo` scope

### Issue: "Port already in use"
**Solution:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

---

## File Structure 📁

After setup, your directory should look like:

```
github-branch-analysis/
├── input_flask_enhanced_v2.py      # Flask API backend
├── streamlit_dashboard_v3.py        # Streamlit frontend
├── requirements.txt                 # Python dependencies
├── README.md                        # Full documentation
├── SETUP_GUIDE.md                   # This file
└── .gitignore                       # Git ignore file
```

---

## Next Steps 📚

1. **Read the full README.md** for detailed feature explanations
2. **Try different repositories** to see various patterns
3. **Explore all visualizations** and understand the data
4. **Check conflict zones** before merging branches

---

## Recommended Test Repositories

| Repository | Why Use It |
|------------|------------|
| `kubernetes/kubernetes` | Large, many branches, active |
| `facebook/react` | Good merge patterns |
| `microsoft/vscode` | High activity |
| `tensorflow/tensorflow` | Complex branching |

---

## Stopping the Application 🛑

1. Press `Ctrl + C` in Terminal 1 (Flask)
2. Press `Ctrl + C` in Terminal 2 (Streamlit)

---

## Getting Help 💬

- **Check README.md** for detailed documentation
- **Check Troubleshooting section** in README
- **Create GitHub issue** for bugs
- **Email:** your.email@example.com

---

## Security Reminder 🔒

**NEVER commit your GitHub token to version control!**

Add to `.gitignore`:
```
# GitHub token
input_flask_enhanced_v2.py
*.env

# Or use environment variables instead
```

Better approach - Use environment variables:
```python
import os
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
```

Then set in terminal:
```bash
# Windows
set GITHUB_TOKEN=your_token_here

# Linux/Mac
export GITHUB_TOKEN=your_token_here
```

---

**Setup Complete! 🎉**

You're ready to analyze GitHub repositories and detect conflicts!
