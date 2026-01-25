# 🔍 GitHub Repository Branch Analysis & Visualization Dashboard

A comprehensive web application for analyzing GitHub repository branches, detecting potential merge conflicts, and visualizing development patterns.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Features Breakdown](#features-breakdown)
- [Screenshots](#screenshots)
- [Technologies Used](#technologies-used)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## 🎯 Overview

This project provides a powerful visualization and analysis tool for GitHub repositories, helping development teams:
- Track branch creation and ownership
- Identify potential merge conflicts before they happen
- Analyze branch divergence and lineage
- Monitor team collaboration patterns
- Detect conflict-prone files (hotspots)
- Review merge patterns and activity

**Perfect for:** DevOps teams, Project managers, Development leads, and anyone managing multi-developer repositories.

---

## ✨ Features

### 🌿 **Branch Analysis**
- **Branch Lineage Tracking**: Visualize parent-child relationships between branches
- **Creator Information**: See who created each branch and when
- **Latest Activity**: Monitor the most recent commits per branch
- **Divergence Analysis**: Track how far branches are ahead/behind the main branch
- **Activity Timeline**: Visual timeline of branch development

### 🔀 **Merge Intelligence**
- **Merge Pattern Analysis**: Understand when and how branches are merged
- **Merge Frequency Tracking**: Monitor merge activity over time
- **Top Contributors**: Identify key merge managers

### ⚠️ **Conflict Detection** (Most Important!)
- **Conflict Zone Identification**: Detect files modified by multiple commits
- **Hotspot Analysis**: Visual ranking of high-risk files
- **Risk Assessment**: Automatic flagging of files with 5+ modifications
- **Conflict Prediction**: Proactive warnings before merging

### 📊 **Interactive Visualizations**
- Repository overview metrics
- Branch distribution by creator (Pie Chart)
- Branch divergence comparison (Bar Chart)
- Activity timeline (Scatter Plot)
- Merge activity trends (Line Chart)
- Conflict hotspots (Horizontal Bar Chart)
- File change distribution (Pie Chart)

### 🎨 **User Experience**
- Real-time progress indicators
- Intelligent timeout handling (120 seconds)
- Processing time display
- Professional error messages
- Responsive design for all screen sizes

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   User Browser                               │
│              (Streamlit Frontend)                            │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ HTTP Request
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  Flask API Server                            │
│              (Backend REST API)                              │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ PyGithub Library
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  GitHub API                                  │
│         (Repository Data Source)                             │
└─────────────────────────────────────────────────────────────┘
```

**Architecture Components:**

1. **Frontend (Streamlit)**: Interactive web interface with visualizations
2. **Backend (Flask API)**: REST API for data processing and GitHub integration
3. **Data Source (GitHub API)**: Real-time repository data via PyGithub
4. **Visualization Layer (Plotly)**: Interactive charts and graphs

---

## 📦 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- GitHub Personal Access Token
- Internet connection (for GitHub API access)

---

## 🚀 Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/github-branch-analysis.git
cd github-branch-analysis
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**requirements.txt contents:**
```
streamlit==1.31.0
flask==3.0.0
requests==2.31.0
pandas==2.1.4
plotly==5.18.0
PyGithub==2.1.1
```

---

## ⚙️ Configuration

### 1. Generate GitHub Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `read:org` (Read org and team membership)
4. Generate token and copy it

### 2. Update Flask API Configuration

Edit `input_flask_enhanced_v2.py`:

```python
# Line 9 - Replace with your token
GITHUB_TOKEN = 'your_github_personal_access_token_here'
```

⚠️ **Security Note:** Never commit your token to GitHub. Use environment variables in production:

```python
import os
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
```

### 3. Configure Port (Optional)

**Flask API (default: 5000):**
```python
# Last line in input_flask_enhanced_v2.py
app.run(debug=True, port=5000)
```

**Streamlit (default: 8501):**
```bash
streamlit run streamlit_dashboard_v3.py --server.port 8501
```

---

## 🎮 Usage

### Starting the Application

**Terminal 1 - Start Flask API:**
```bash
python input_flask_enhanced_v2.py
```

You should see:
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

**Terminal 2 - Start Streamlit Dashboard:**
```bash
streamlit run streamlit_dashboard_v3.py
```

Browser will automatically open at: `http://localhost:8501`

### Using the Dashboard

1. **Enter Repository Details:**
   - GitHub Owner: `kubernetes`
   - Repository Name: `kubernetes`

2. **Click "Fetch & Analyze Repository"**
   - Watch the progress bar
   - Wait for data processing (20-60 seconds for large repos)

3. **Explore Visualizations:**
   - Scroll through all sections
   - Interact with charts (hover, zoom, filter)
   - Check conflict zones before merging

### Recommended Test Repositories

| Repository | Owner | Repo Name | Why Use It |
|------------|-------|-----------|------------|
| Kubernetes | `kubernetes` | `kubernetes` | Large, active, many branches |
| React | `facebook` | `react` | Popular, good merge patterns |
| TensorFlow | `tensorflow` | `tensorflow` | Complex branching strategy |
| VS Code | `microsoft` | `vscode` | High activity, many contributors |

---

## 🔍 Features Breakdown

### 1. Repository Overview
- **Metrics Displayed:**
  - Total Branches
  - Open Issues
  - Forks
  - Stars
- **Purpose:** Quick health check of repository

### 2. Branch Information & Creator Details
- **Data Shown:**
  - Branch name
  - Creator name and email
  - Creation date
  - Latest commit author
  - Latest commit date
  - Latest commit message
- **Purpose:** Track branch ownership and activity

### 3. Branch Distribution by Creator
- **Visualization:** Pie Chart
- **Insight:** See which developers create most branches
- **Use Case:** Identify work distribution and potential bottlenecks

### 4. Branch Lineage & Relationships
- **Data Shown:**
  - Parent branch
  - Commits ahead (new work)
  - Commits behind (outdated by)
  - Relationship type
- **Purpose:** Understand branch hierarchy and divergence

### 5. Branch Divergence Analysis
- **Visualization:** Grouped Bar Chart
- **Green Bars:** Commits ahead (new commits)
- **Red Bars:** Commits behind (missing updates)
- **Use Case:** Identify branches needing updates before merge

### 6. Latest Activity per Branch
- **Data Shown:**
  - Recent commits count
  - Last activity timestamp
  - Active contributors
- **Purpose:** Find stale branches for cleanup

### 7. Branch Activity Timeline
- **Visualization:** Scatter Plot
- **X-axis:** Time
- **Y-axis:** Branch names
- **Bubble size:** Commit count
- **Color:** Contributors count
- **Use Case:** Visual timeline of development activity

### 8. Merge Patterns & History
- **Data Shown:**
  - Merge commit SHA
  - Author
  - Date
  - Message
  - Parent count
- **Purpose:** Understand merge frequency and patterns

### 9. Merge Activity Timeline
- **Visualization:** Line Chart
- **Shows:** Merge frequency over time
- **Use Case:** Identify release patterns and merge velocity

### 10. Top Merge Contributors
- **Visualization:** Bar Chart
- **Shows:** Developers ranked by merge count
- **Use Case:** Identify merge managers and potential bottlenecks

### 11. Potential Conflict Zones ⚠️ (CRITICAL!)
- **Data Shown:**
  - Filename
  - Modification count (how many commits touched it)
  - Total changes (lines added/deleted)
  - Commit SHAs
- **Purpose:** Predict merge conflicts BEFORE they happen
- **Risk Levels:**
  - 1-2 mods: ✅ Low risk
  - 3-4 mods: ⚠️ Moderate risk
  - 5-7 mods: 🟠 High risk
  - 8+ mods: 🚨 Critical risk

### 12. Conflict Hotspot Analysis
- **Visualization:** Horizontal Bar Chart
- **Color Coding:** Red (high risk) to Yellow (low risk)
- **Shows:** Top 15 most-modified files
- **Use Case:** Focus code review on high-risk files

### 13. High-Risk Files Alert
- **Alert Shown:** Files modified 5+ times
- **Purpose:** Immediate attention to conflict-prone files
- **Action Items:** Review before any merge

### 14. Recent Commits
- **Data Shown:**
  - Commit SHA (shortened)
  - Author
  - Date
  - Message
- **Purpose:** Understand recent development activity

### 15. Files Changed Metrics
- **Metrics:**
  - Total files changed
  - Total lines added
  - Total lines deleted
- **Purpose:** Measure change volume and code growth

### 16. File Change Status Distribution
- **Visualization:** Pie Chart
- **Categories:**
  - Modified (existing files changed)
  - Added (new files created)
  - Removed (files deleted)
  - Renamed (files moved/renamed)
- **Purpose:** Understand type of changes happening

---

## 📸 Screenshots

### Dashboard Overview
```
┌─────────────────────────────────────────────────────────────┐
│  🔍 GitHub Repository Branch Analysis & Visualization        │
├─────────────────────────────────────────────────────────────┤
│  GitHub Owner: [kubernetes     ]                             │
│  Repository:   [kubernetes     ]                             │
│  [🚀 Fetch & Analyze Repository]                             │
├─────────────────────────────────────────────────────────────┤
│  📊 Repository Overview                                      │
│  ┌───────┬───────┬───────┬───────┐                          │
│  │  42   │  156  │  892  │12,345 │                          │
│  │Branches│Issues│ Forks │ Stars │                          │
│  └───────┴───────┴───────┴───────┘                          │
└─────────────────────────────────────────────────────────────┘
```

### Conflict Zones (Most Important!)
```
┌─────────────────────────────────────────────────────────────┐
│  ⚠️ Potential Conflict Zones                                 │
├─────────────────────────────────────────────────────────────┤
│  Filename              Mods  Changes  Commits               │
│  config/database.js     12    340     [a1b2, c3d4, ...]     │
│  src/models/user.js      8    156     [e5f6, g7h8, ...]     │
│  utils/api.js            6     89     [i9j0, k1l2, ...]     │
├─────────────────────────────────────────────────────────────┤
│  🔥 Conflict Hotspot Analysis                                │
│  config/database.js     ████████████ (12 mods)              │
│  src/models/user.js     ████████ (8 mods)                   │
│  utils/api.js           ██████ (6 mods)                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technologies Used

### Backend
- **Flask 3.0.0**: Lightweight web framework for REST API
- **PyGithub 2.1.1**: Python library for GitHub API v3
- **Python 3.8+**: Core programming language

### Frontend
- **Streamlit 1.31.0**: Rapid web app framework for data applications
- **Plotly 5.18.0**: Interactive visualization library
- **Pandas 2.1.4**: Data manipulation and analysis

### APIs
- **GitHub REST API v3**: Repository data source

### Development Tools
- **Requests 2.31.0**: HTTP library for API calls
- **JSON**: Data format for API communication

---

## 🔌 API Endpoints

### GET `/repo-details/<owner>/<repo_name>`

**Description:** Fetches comprehensive branch analysis for a repository

**Parameters:**
- `owner` (string): GitHub repository owner
- `repo_name` (string): Repository name

**Example Request:**
```bash
curl http://localhost:5000/repo-details/kubernetes/kubernetes
```

**Response Format:**
```json
{
  "repository": {
    "name": "kubernetes/kubernetes",
    "description": "Production-Grade Container Scheduling...",
    "default_branch": "master",
    "total_branches": 42,
    "open_issues": 156,
    "forks": 892,
    "stars": 12345
  },
  "branches": [
    {
      "name": "master",
      "commit_sha": "abc123...",
      "creator": "John Doe",
      "creator_email": "john@example.com",
      "created_date": "2024-01-15T10:30:00Z",
      "latest_commit_date": "2026-01-24T14:22:00Z",
      "latest_commit_message": "Fix authentication bug",
      "latest_commit_author": "Jane Smith"
    }
  ],
  "branch_lineage": [
    {
      "branch": "feature/new-ui",
      "parent_branch": "master",
      "diverged_from": "master",
      "commits_ahead": 15,
      "commits_behind": 3,
      "relationship": "feature branch"
    }
  ],
  "branch_activity": [...],
  "recent_commits": [...],
  "files_changed": [...],
  "merge_patterns": [...],
  "conflict_zones": [
    {
      "filename": "config/database.js",
      "modification_count": 12,
      "total_changes": 340,
      "commits": ["a1b2c3", "d4e5f6", ...]
    }
  ],
  "processing_time": "23.45s",
  "note": "Limited to 20 branches and 10 commits for performance"
}
```

**Response Codes:**
- `200 OK`: Successful request
- `404 Not Found`: Repository doesn't exist
- `401 Unauthorized`: Invalid GitHub token
- `403 Forbidden`: Rate limit exceeded
- `500 Internal Server Error`: Server error

---

## 🐛 Troubleshooting

### Issue 1: "Failed to fetch data from Flask API"

**Cause:** Flask server not running

**Solution:**
```bash
# Terminal 1
python input_flask_enhanced_v2.py
```

### Issue 2: "ModuleNotFoundError: No module named 'streamlit'"

**Cause:** Dependencies not installed

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue 3: "Request timed out. The repository might be too large."

**Cause:** Repository has too many branches/commits

**Solution:**
1. Try a smaller repository
2. Increase timeout in `streamlit_dashboard_v3.py`:
   ```python
   response = requests.get(url, timeout=300)  # 5 minutes
   ```
3. Reduce branch/commit limits in Flask API

### Issue 4: "403 Forbidden - API rate limit exceeded"

**Cause:** GitHub API rate limit reached

**Solution:**
1. Wait 1 hour for rate limit reset
2. Use authenticated token (increases limit from 60 to 5000/hour)
3. Check rate limit:
   ```python
   print(g.get_rate_limit())
   ```

### Issue 5: "401 Unauthorized"

**Cause:** Invalid GitHub token

**Solution:**
1. Generate new token at: https://github.com/settings/tokens
2. Update `GITHUB_TOKEN` in `input_flask_enhanced_v2.py`
3. Ensure token has `repo` scope

### Issue 6: Charts not displaying

**Cause:** Plotly not installed or JavaScript disabled

**Solution:**
```bash
pip install --upgrade plotly
```

### Issue 7: "Port already in use"

**Cause:** Flask already running or port occupied

**Solution:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Issue 8: Slow performance

**Cause:** Large repository with many branches

**Solutions:**
1. Reduce limits in Flask API:
   ```python
   branches_to_process = all_branches[:10]  # Reduce from 20
   commits = list(repo.get_commits()[:5])   # Reduce from 10
   ```
2. Use caching (see Future Enhancements)

---

## 🚀 Future Enhancements

### Planned Features

1. **Caching Layer**
   - Redis integration for API response caching
   - Reduce repeated GitHub API calls
   - Faster subsequent loads

2. **Database Storage**
   - PostgreSQL for historical data
   - Track branch lifecycle over time
   - Trend analysis

3. **Real-time Updates**
   - WebSocket integration
   - Live branch activity monitoring
   - Push notifications for conflicts

4. **Advanced Analytics**
   - Machine learning for conflict prediction
   - Developer productivity metrics
   - Code churn analysis

5. **Export Features**
   - PDF report generation
   - CSV data export
   - Automated email reports

6. **Multi-Repository Dashboard**
   - Compare multiple repositories
   - Organization-wide analytics
   - Cross-repo conflict detection

7. **Authentication System**
   - User login/logout
   - Save favorite repositories
   - Personalized dashboards

8. **Integration Features**
   - Slack notifications
   - JIRA integration
   - CI/CD pipeline integration

9. **Advanced Visualizations**
   - Network graph of branch relationships
   - Heatmap of file modifications
   - 3D timeline visualization

10. **Performance Optimizations**
    - Async API calls
    - Parallel processing
    - Progressive loading

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/github-branch-analysis.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Add features
   - Fix bugs
   - Improve documentation

4. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```

5. **Push to branch**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request**

### Contribution Guidelines

- Follow PEP 8 style guide for Python
- Add docstrings to functions
- Include unit tests for new features
- Update README for new features
- Keep commits atomic and well-described

---

## 📄 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2026 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👤 Author

**[S.Shanmuga Priya]**
- GitHub: [@ShanmugapriyaS-ai](https://github.com/ShanmugapriyaS-ai)
- Email: priyadurgaps@gmail.com
- LinkedIn: [Your LinkedIn](https://www.linkedin.com/in/shanmuga-priya-9b9a9b209)

---

## 🙏 Acknowledgments

- **GitHub API** for providing comprehensive repository data
- **Streamlit** team for the amazing framework
- **Plotly** for interactive visualizations
- **Flask** community for the lightweight web framework
- **PyGithub** maintainers for the excellent library
- **Kubernetes** project for being an excellent test repository

---

## 📊 Project Statistics

- **Lines of Code:** ~800 (Python)
- **Files:** 2 main files (Flask API + Streamlit Dashboard)
- **Dependencies:** 6 core packages
- **Visualizations:** 10+ interactive charts
- **Features:** 16 major analysis sections

---

## 🎓 Use Cases

### For Development Teams
- Monitor branch health
- Identify stale branches for cleanup
- Predict merge conflicts
- Track team collaboration patterns

### For Project Managers
- View development velocity
- Monitor team workload distribution
- Identify bottlenecks
- Track release readiness

### For DevOps Engineers
- Analyze merge patterns
- Optimize branching strategy
- Monitor repository health
- Improve CI/CD pipeline

### For Tech Leads
- Review code ownership
- Ensure best practices
- Manage code reviews
- Plan refactoring efforts

---

## 📞 Support

For issues, questions, or suggestions:

1. **GitHub Issues:** [Create an issue](https://github.com/ShanmugapriyaS-ai/github-branch-analysis/issues)
2. **Email:** priyadurgaps@gmail.com
3. **Documentation:** Check this README thoroughly

---


## 📝 Changelog

### Version 3.0 (Current)
- ✅ Added progress indicators
- ✅ Implemented timeout handling
- ✅ Added processing time display
- ✅ Enhanced error messages
- ✅ Improved user experience

### Version 2.0
- ✅ Complete branch analysis
- ✅ Conflict zone detection
- ✅ Interactive visualizations
- ✅ Merge pattern analysis

### Version 1.0
- ✅ Basic repository overview
- ✅ Branch listing
- ✅ Commit history

---

## ⭐ Star History

If you find this project useful, please consider giving it a star on GitHub!

---

**Made with ❤️ for better GitHub repository management**

---

*Last Updated: January 2026*
