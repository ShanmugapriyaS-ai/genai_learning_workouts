import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

st.set_page_config(page_title="GitHub Branch Analysis Dashboard", layout="wide")
st.title("🔍 GitHub Repository Branch Analysis & Visualization")

# -------- Inputs --------
col1, col2 = st.columns(2)
with col1:
    owner = st.text_input("GitHub Owner", "kubernetes")
with col2:
    repo = st.text_input("Repository Name", "kubernetes")

if st.button("🚀 Fetch & Analyze Repository", type="primary"):
    progress_text = st.empty()
    progress_bar = st.progress(0)
    
    progress_text.text("⏳ Connecting to Flask API...")
    progress_bar.progress(10)
    
    url = f"http://localhost:5000/repo-details/{owner}/{repo}"
    
    progress_text.text("🔍 Fetching repository data... (this may take 30-60 seconds for large repos)")
    progress_bar.progress(30)
    
    try:
        response = requests.get(url, timeout=120)  # 2 minute timeout
        progress_bar.progress(90)
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. The repository might be too large. Try a smaller repository.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Connection error: {str(e)}")
        st.stop()
    
    progress_bar.progress(100)
    progress_text.text("✅ Data fetched successfully!")
    time.sleep(0.5)
    progress_text.empty()
    progress_bar.empty()

    if response.status_code != 200:
        st.error("Failed to fetch data from Flask API. Make sure the Flask server is running!")
        st.stop()

    data = response.json()

    # -------- Repository Info --------
    st.header("📊 Repository Overview")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Branches", data['repository']['total_branches'])
    with col2:
        st.metric("Open Issues", data['repository']['open_issues'])
    with col3:
        st.metric("Forks", data['repository']['forks'])
    with col4:
        st.metric("Stars", data['repository']['stars'])
    
    st.write(f"**Name:** {data['repository']['name']}")
    st.write(f"**Description:** {data['repository']['description']}")
    st.write(f"**Default Branch:** {data['repository']['default_branch']}")
    
    st.divider()

    # -------- Branch Information with Creator Details --------
    st.header("🌿 Branch Information & Creator Details")
    
    branch_df = pd.DataFrame(data["branches"])
    branch_df["created_date"] = pd.to_datetime(branch_df["created_date"])
    branch_df["latest_commit_date"] = pd.to_datetime(branch_df["latest_commit_date"])
    
    # Display branches with key information
    display_cols = ["name", "creator", "created_date", "latest_commit_author", "latest_commit_date", "latest_commit_message"]
    st.dataframe(
        branch_df[display_cols].style.format({
            "created_date": lambda x: x.strftime("%Y-%m-%d %H:%M"),
            "latest_commit_date": lambda x: x.strftime("%Y-%m-%d %H:%M")
        }),
        use_container_width=True,
        height=300
    )
    
    # Branch creators pie chart
    st.subheader("👥 Branch Distribution by Creator")
    creator_counts = branch_df['creator'].value_counts().reset_index()
    creator_counts.columns = ['Creator', 'Count']
    fig_creators = px.pie(creator_counts, values='Count', names='Creator', 
                          title='Branches Created by Each Developer')
    st.plotly_chart(fig_creators, use_container_width=True)
    
    st.divider()

    # -------- Branch Lineage --------
    st.header("🌳 Branch Lineage & Relationships")
    
    lineage_df = pd.DataFrame(data["branch_lineage"])
    st.dataframe(lineage_df, use_container_width=True, height=300)
    
    # Visualize branch relationships
    if "commits_ahead" in lineage_df.columns and "commits_behind" in lineage_df.columns:
        st.subheader("📈 Branch Divergence Analysis")
        
        # Filter out the main branch for clearer visualization
        divergence_df = lineage_df[lineage_df["relationship"] != "main branch"].copy()
        
        if not divergence_df.empty:
            fig_divergence = go.Figure()
            
            fig_divergence.add_trace(go.Bar(
                name='Commits Ahead',
                x=divergence_df['branch'],
                y=divergence_df['commits_ahead'],
                marker_color='lightgreen'
            ))
            
            fig_divergence.add_trace(go.Bar(
                name='Commits Behind',
                x=divergence_df['branch'],
                y=divergence_df['commits_behind'],
                marker_color='lightcoral'
            ))
            
            fig_divergence.update_layout(
                title='Branch Divergence from Default Branch',
                xaxis_title='Branch Name',
                yaxis_title='Number of Commits',
                barmode='group',
                height=400
            )
            
            st.plotly_chart(fig_divergence, use_container_width=True)
        else:
            st.info("No divergence data available for visualization")
    
    st.divider()

    # -------- Branch Activity --------
    st.header("⚡ Latest Activity per Branch")
    
    activity_df = pd.DataFrame(data["branch_activity"])
    activity_df["last_activity"] = pd.to_datetime(activity_df["last_activity"])
    activity_df = activity_df.sort_values("last_activity", ascending=False)
    
    st.dataframe(
        activity_df.style.format({
            "last_activity": lambda x: x.strftime("%Y-%m-%d %H:%M")
        }),
        use_container_width=True,
        height=300
    )
    
    # Timeline of branch activity
    st.subheader("📅 Branch Activity Timeline")
    fig_timeline = px.scatter(activity_df, x='last_activity', y='branch_name', 
                              size='recent_commits_count', color='active_contributors',
                              title='Branch Activity Over Time',
                              labels={'last_activity': 'Last Activity Date', 
                                     'branch_name': 'Branch Name',
                                     'active_contributors': 'Contributors'})
    fig_timeline.update_layout(height=400)
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    st.divider()

    # -------- Merge Patterns --------
    st.header("🔀 Merge Patterns & History")
    
    if data["merge_patterns"]:
        merge_df = pd.DataFrame(data["merge_patterns"])
        merge_df["date"] = pd.to_datetime(merge_df["date"])
        merge_df = merge_df.sort_values("date", ascending=False)
        
        st.write(f"**Total Merge Commits Found:** {len(merge_df)}")
        
        display_merge_cols = ["sha", "author", "date", "message", "parent_count"]
        st.dataframe(
            merge_df[display_merge_cols].style.format({
                "date": lambda x: x.strftime("%Y-%m-%d %H:%M"),
                "sha": lambda x: x[:7]
            }),
            use_container_width=True,
            height=300
        )
        
        # Merge activity over time
        st.subheader("📊 Merge Activity Timeline")
        merge_counts = merge_df.groupby(merge_df['date'].dt.date).size().reset_index()
        merge_counts.columns = ['Date', 'Merge Count']
        
        fig_merge = px.line(merge_counts, x='Date', y='Merge Count', 
                           title='Merge Operations Over Time',
                           markers=True)
        st.plotly_chart(fig_merge, use_container_width=True)
        
        # Top merge contributors
        st.subheader("👤 Top Merge Contributors")
        merge_authors = merge_df['author'].value_counts().reset_index()
        merge_authors.columns = ['Author', 'Merge Count']
        fig_merge_authors = px.bar(merge_authors.head(10), x='Author', y='Merge Count',
                                   title='Top 10 Developers by Merge Count')
        st.plotly_chart(fig_merge_authors, use_container_width=True)
    else:
        st.info("No merge commits found in recent history")
    
    st.divider()

    # -------- Conflict Zones --------
    st.header("⚠️ Potential Conflict Zones")
    st.write("Files modified by multiple commits - potential areas for conflicts")
    
    if data["conflict_zones"]:
        conflict_df = pd.DataFrame(data["conflict_zones"])
        
        # Display top conflict zones
        st.dataframe(conflict_df, use_container_width=True, height=400)
        
        # Visualize conflict hotspots
        st.subheader("🔥 Conflict Hotspot Analysis")
        fig_conflicts = px.bar(conflict_df.head(15), 
                              x='modification_count', 
                              y='filename',
                              orientation='h',
                              title='Top 15 Files by Modification Count',
                              labels={'modification_count': 'Number of Modifications', 
                                     'filename': 'File Path'},
                              color='total_changes',
                              color_continuous_scale='Reds')
        fig_conflicts.update_layout(height=500)
        st.plotly_chart(fig_conflicts, use_container_width=True)
        
        # High-risk files alert
        high_risk = conflict_df[conflict_df['modification_count'] >= 5]
        if not high_risk.empty:
            st.warning(f"⚠️ **{len(high_risk)} files** have been modified 5+ times - High risk for conflicts!")
            with st.expander("View High-Risk Files"):
                st.dataframe(high_risk, use_container_width=True)
    else:
        st.success("✅ No significant conflict zones detected")
    
    st.divider()

    # -------- Recent Commits --------
    st.header("💬 Recent Commits")
    commits_df = pd.DataFrame(data["recent_commits"])
    commits_df["date"] = pd.to_datetime(commits_df["date"])
    commits_df = commits_df.sort_values("date", ascending=False)
    
    display_commit_cols = ["sha", "author", "date", "message"]
    st.dataframe(
        commits_df[display_commit_cols].style.format({
            "date": lambda x: x.strftime("%Y-%m-%d %H:%M"),
            "sha": lambda x: x[:7]
        }),
        use_container_width=True,
        height=300
    )
    
    st.divider()

    # -------- Files Changed --------
    st.header("📁 Files Changed in Recent Commits")
    files_df = pd.DataFrame(data["files_changed"])
    
    # Summary statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Files Changed", len(files_df))
    with col2:
        st.metric("Total Additions", files_df['additions'].sum())
    with col3:
        st.metric("Total Deletions", files_df['deletions'].sum())
    
    st.dataframe(files_df, use_container_width=True, height=400)
    
    # File change types distribution
    st.subheader("📊 File Change Status Distribution")
    status_counts = files_df['status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    fig_status = px.pie(status_counts, values='Count', names='Status',
                       title='Distribution of File Change Types')
    st.plotly_chart(fig_status, use_container_width=True)

# -------- Instructions --------
with st.sidebar:
    st.header("📖 Instructions")
    st.write("""
    1. Enter GitHub repository owner and name
    2. Click 'Fetch & Analyze Repository'
    3. Review all analysis sections:
       - **Branch Info**: See who created each branch
       - **Branch Lineage**: Understand parent-child relationships
       - **Latest Activity**: Track recent commits per branch
       - **Merge Patterns**: Analyze merge history
       - **Conflict Zones**: Identify files at risk for conflicts
    
    **Note:** Make sure Flask API is running on localhost:5000
    """)
    
    st.divider()
    
    st.header("🔧 Suggested Repositories")
    st.write("""
    Try these popular repositories:
    - **kubernetes/kubernetes**
    - **facebook/react**
    - **tensorflow/tensorflow**
    - **microsoft/vscode**
    """)
