# 🚀 Quick Reference Card

## One-Page Guide for GitHub Branch Analysis Dashboard

---

## 📦 Installation (60 seconds)

```bash
pip install streamlit flask requests pandas plotly PyGithub
```

---

## 🔑 Get GitHub Token (2 minutes)

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Check `repo` scope
4. Copy token
5. Paste in `flask_branch_analysis.py` line 9

---

## ▶️ Run Application

**Terminal 1:**
```bash
python flask_branch_analysis.py
```

**Terminal 2:**
```bash
streamlit run streamlit_dashboard.py
```

**Open:** http://localhost:8501

---

## 🧪 Test Repositories

| Owner | Repo | Why |
|-------|------|-----|
| `kubernetes` | `kubernetes` | Large, many branches |
| `facebook` | `react` | Good patterns |
| `microsoft` | `vscode` | High activity |

---

## 📊 Key Features

### 1. Branch Analysis
- Who created each branch
- When created
- Latest activity
- Divergence from main

### 2. Conflict Detection ⚠️
- Files modified by multiple commits
- Risk assessment
- Hotspot visualization

### 3. Merge Patterns
- Merge frequency
- Top contributors
- Activity timeline

---

## 🎯 Important Visualizations

| Visualization | What It Shows | Why Important |
|---------------|---------------|---------------|
| **Conflict Zones** | High-risk files | Prevent merge conflicts |
| **Branch Divergence** | Ahead/Behind commits | Know when to merge |
| **Activity Timeline** | Branch freshness | Find stale branches |
| **Merge Patterns** | Integration velocity | Team efficiency |

---

## ⚠️ Before Merging ANY Branch

1. Check **Conflict Zones** section
2. Look for your modified files
3. See if others modified same files
4. Pull main if commits_behind > 10
5. Test thoroughly

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't connect to API | Start Flask first |
| 401 Error | Check GitHub token |
| Timeout | Try smaller repo |
| Module not found | Run `pip install -r requirements.txt` |
| Port in use | Kill process on port 5000 |

---

## 🔧 Commands Cheat Sheet

### Stop Application
```bash
Ctrl + C  (in both terminals)
```

### Check Python Version
```bash
python --version
```

### Kill Port 5000 (if stuck)
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Reinstall Dependencies
```bash
pip install --upgrade -r requirements.txt
```

---

## 📁 File Structure

```
github-branch-analysis/
├── flask_branch_analysis.py             ← Backend API
├── streamlit_dashboard.py               ← Frontend UI
├── requirements.txt                     ← Dependencies
├── README.md                            ← Full docs
└── .gitignore                           ← Protect token
```

---

## 🎨 Understanding Visualizations

### Branch Divergence Chart
- **Green bars** = New work (commits ahead)
- **Red bars** = Missing updates (commits behind)
- **Action:** If red > 20, pull main first

### Conflict Zones Table
- **Mod count 1-2** = ✅ Safe
- **Mod count 3-4** = ⚠️ Moderate risk
- **Mod count 5+** = 🚨 High risk

### Activity Timeline
- **Right side** = Recent activity
- **Left side** = Stale branches
- **Large bubbles** = Many commits

---

## 💡 Pro Tips

1. **Before Demo:**
   - Test with 2 different repos
   - Know your talking points
   - Have token ready

2. **Conflict Detection:**
   - Focus on files with 5+ modifications
   - Check before every merge
   - Coordinate with team

3. **Performance:**
   - Use smaller repos for demos
   - Default limits: 20 branches, 10 commits
   - Adjust in Flask API if needed

4. **Security:**
   - Never commit actual token
   - Use .gitignore
   - Use environment variables

---

## 📊 Data Interpretation

### Healthy Repository
- ✅ Balanced branch creators
- ✅ Recent merge activity
- ✅ Few conflict zones
- ✅ Active branches < 30 days old

### Needs Attention
- ⚠️ One person creates 50%+ branches
- ⚠️ No merges in 7+ days
- ⚠️ Many files with 5+ modifications
- ⚠️ Branches 90+ days old

---

## 🎓 For Presentation

### Opening (30 seconds)
"I built a GitHub branch analysis dashboard that helps teams prevent merge conflicts and manage branches effectively."

### Key Points (2 minutes)
1. **Problem:** Merge conflicts waste time
2. **Solution:** Predict conflicts before merging
3. **How:** Analyzes file modifications across branches
4. **Result:** Proactive conflict management

### Demo Flow (3 minutes)
1. Enter repository details
2. Show progress bar
3. Highlight repository overview
4. Demonstrate conflict detection
5. Explain branch divergence
6. Show merge patterns

### Closing (30 seconds)
"This tool provides visibility into repository health and helps teams work more efficiently."

---

## 🚨 Common Mistakes to Avoid

❌ Committing GitHub token to Git
❌ Not testing before submission
❌ Missing requirements.txt
❌ Hardcoded file paths
❌ No error handling
❌ Poor variable names
❌ Uncommented complex code

✅ Use .gitignore
✅ Test on clean environment
✅ Include all dependencies
✅ Use relative paths
✅ Handle all errors gracefully
✅ Descriptive names
✅ Comment complex logic

---

## 📞 Emergency Contacts

**Documentation:**
- Full docs: README.md
- Setup: SETUP_GUIDE.md
- Checklist: SUBMISSION_CHECKLIST.md

**Online Resources:**
- Streamlit: https://docs.streamlit.io
- Flask: https://flask.palletsprojects.com
- PyGithub: https://pygithub.readthedocs.io
- Plotly: https://plotly.com/python

---

## ⏱️ Time Estimates

| Task | Time |
|------|------|
| Installation | 2 min |
| Get GitHub token | 3 min |
| First run | 1 min |
| Test with repo | 2 min |
| Understand features | 10 min |
| Prepare demo | 15 min |
| **Total** | **~30 min** |

---

## 🎯 Assignment Requirements Met

- ✅ Branch lineage tracking
- ✅ Creator information
- ✅ Latest activity monitoring
- ✅ Merge pattern analysis
- ✅ Conflict zone detection
- ✅ Interactive visualizations
- ✅ Professional UI/UX
- ✅ Error handling
- ✅ Documentation

---

## 🏆 Success Metrics

Your dashboard successfully:
1. Analyzes GitHub repositories ✅
2. Visualizes branch relationships ✅
3. Detects potential conflicts ✅
4. Provides actionable insights ✅
5. Handles errors gracefully ✅
6. Has professional appearance ✅

---

## 📝 Quick Notes Space

Use this space for your own notes:

**GitHub Token:** (first/last 4 chars only)
```
ghp_xxxx...xxxx
```

**Test Repos Used:**
1. ______________________
2. ______________________
3. ______________________

**Known Issues:**
- ______________________
- ______________________

**Demo Talking Points:**
- ______________________
- ______________________
- ______________________

---

## ✅ Pre-Submission Checklist

- [ ] Tested on clean environment
- [ ] README.md complete
- [ ] No tokens in code
- [ ] All files committed
- [ ] Repository is public
- [ ] Documentation clear
- [ ] Screenshots ready (optional)
- [ ] Demo prepared

---

**Ready to Submit!** 🚀

**Last Updated:** January 2026
**Version:** 3.0 (Enhanced)
