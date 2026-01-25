from flask import Flask, jsonify
from github import Github
from datetime import timezone
from collections import defaultdict
import time

app = Flask(__name__)

GITHUB_TOKEN = 'YOUR_GITHUB_PERSONAL_ACCESS_TOKEN_HERE'
g = Github(GITHUB_TOKEN)

@app.route("/repo-details/<owner>/<repo_name>")
def repo_details(owner, repo_name):
    start_time = time.time()
    repo = g.get_repo(f"{owner}/{repo_name}")

    # -------- Branches with Enhanced Information (OPTIMIZED) --------
    branches = []
    branch_commits_map = {}
    
    all_branches = list(repo.get_branches())
    print(f"Found {len(all_branches)} branches")
    
    # Limit to first 20 branches for faster loading
    branches_to_process = all_branches[:20]
    
    for idx, b in enumerate(branches_to_process):
        print(f"Processing branch {idx + 1}/{len(branches_to_process)}: {b.name}")
        
        latest_commit = b.commit
        
        # Simplified approach - use latest commit info instead of fetching all commits
        try:
            creator = latest_commit.commit.author.name if latest_commit.commit.author else "Unknown"
            creator_email = latest_commit.commit.author.email if latest_commit.commit.author else "Unknown"
            created_date = latest_commit.commit.author.date.astimezone(timezone.utc).isoformat()
        except Exception as e:
            print(f"Error getting creator info for {b.name}: {e}")
            creator = "Unknown"
            creator_email = "Unknown"
            created_date = "Unknown"
        
        branch_info = {
            "name": b.name,
            "commit_sha": b.commit.sha,
            "creator": creator,
            "creator_email": creator_email,
            "created_date": created_date,
            "latest_commit_date": latest_commit.commit.author.date.astimezone(timezone.utc).isoformat(),
            "latest_commit_message": latest_commit.commit.message[:100],  # Truncate long messages
            "latest_commit_author": latest_commit.commit.author.name if latest_commit.commit.author else "Unknown"
        }
        branches.append(branch_info)
        branch_commits_map[b.name] = latest_commit.sha

    print(f"Branches processed in {time.time() - start_time:.2f}s")

    # -------- Branch Lineage Analysis (OPTIMIZED) --------
    branch_lineage = []
    default_branch = repo.default_branch
    
    # Only compare first 10 branches to default branch
    for branch in branches[:10]:
        if branch["name"] == default_branch:
            lineage_info = {
                "branch": branch["name"],
                "parent_branch": "root",
                "diverged_from": default_branch,
                "commits_ahead": 0,
                "commits_behind": 0,
                "relationship": "main branch"
            }
        else:
            try:
                comparison = repo.compare(default_branch, branch["name"])
                lineage_info = {
                    "branch": branch["name"],
                    "parent_branch": default_branch,
                    "diverged_from": default_branch,
                    "commits_ahead": comparison.ahead_by,
                    "commits_behind": comparison.behind_by,
                    "relationship": "feature/development branch"
                }
            except Exception as e:
                print(f"Error comparing {branch['name']}: {e}")
                lineage_info = {
                    "branch": branch["name"],
                    "parent_branch": "Unknown",
                    "diverged_from": "Unknown",
                    "commits_ahead": 0,
                    "commits_behind": 0,
                    "relationship": "isolated branch"
                }
        
        branch_lineage.append(lineage_info)

    print(f"Lineage analyzed in {time.time() - start_time:.2f}s")

    # -------- Recent Commits (LIMITED) --------
    commits_data = []
    files_data = []
    
    # Reduce from 20 to 10 commits for faster loading
    commits = list(repo.get_commits()[:10])
    print(f"Fetching {len(commits)} commits")

    for idx, c in enumerate(commits):
        try:
            commit_info = {
                "sha": c.sha,
                "author": c.commit.author.name if c.commit.author else "Unknown",
                "email": c.commit.author.email if c.commit.author else "Unknown",
                "date": c.commit.author.date.astimezone(timezone.utc).isoformat(),
                "message": c.commit.message[:200]  # Truncate long messages
            }
            commits_data.append(commit_info)

            # -------- Files changed per commit --------
            for f in c.files:
                files_data.append({
                    "commit_sha": c.sha,
                    "filename": f.filename,
                    "status": f.status,
                    "additions": f.additions,
                    "deletions": f.deletions,
                    "changes": f.changes
                })
        except Exception as e:
            print(f"Error processing commit {idx}: {e}")
            continue

    print(f"Commits processed in {time.time() - start_time:.2f}s")

    # -------- Merge Pattern Analysis --------
    merge_patterns = []
    for c in commits:
        try:
            if len(c.parents) > 1:  # Merge commit
                merge_info = {
                    "sha": c.sha,
                    "author": c.commit.author.name if c.commit.author else "Unknown",
                    "date": c.commit.author.date.astimezone(timezone.utc).isoformat(),
                    "message": c.commit.message[:100],
                    "parent_count": len(c.parents),
                    "parents": [p.sha for p in c.parents]
                }
                merge_patterns.append(merge_info)
        except Exception as e:
            print(f"Error processing merge pattern: {e}")
            continue

    # -------- Conflict Zone Detection --------
    file_modifications = defaultdict(list)
    
    for file_change in files_data:
        file_modifications[file_change["filename"]].append({
            "commit_sha": file_change["commit_sha"],
            "status": file_change["status"],
            "changes": file_change["changes"]
        })
    
    conflict_zones = []
    for filename, modifications in file_modifications.items():
        if len(modifications) > 1:  # File modified by multiple commits
            conflict_zones.append({
                "filename": filename,
                "modification_count": len(modifications),
                "total_changes": sum(m["changes"] for m in modifications),
                "commits": [m["commit_sha"][:7] for m in modifications]
            })
    
    # Sort by modification count
    conflict_zones = sorted(conflict_zones, key=lambda x: x["modification_count"], reverse=True)

    # -------- Branch Activity Summary (SIMPLIFIED) --------
    branch_activity = []
    for branch in branches[:10]:  # Only first 10 branches
        activity = {
            "branch_name": branch["name"],
            "recent_commits_count": 1,  # Simplified - would need more API calls
            "last_activity": branch["latest_commit_date"],
            "active_contributors": 1  # Simplified
        }
        branch_activity.append(activity)

    total_time = time.time() - start_time
    print(f"Total processing time: {total_time:.2f}s")

    return jsonify({
        "repository": {
            "name": repo.full_name,
            "description": repo.description,
            "default_branch": repo.default_branch,
            "total_branches": len(all_branches),
            "open_issues": repo.open_issues_count,
            "forks": repo.forks_count,
            "stars": repo.stargazers_count
        },
        "branches": branches,
        "branch_lineage": branch_lineage,
        "branch_activity": branch_activity,
        "recent_commits": commits_data,
        "files_changed": files_data,
        "merge_patterns": merge_patterns,
        "conflict_zones": conflict_zones[:20],
        "processing_time": f"{total_time:.2f}s",
        "note": "Limited to 20 branches and 10 commits for performance"
    })


if __name__ == "__main__":
    app.run(debug=True)
