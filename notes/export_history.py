import gitlab
from datetime import datetime, timedelta
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the GitLab private token from environment variables
private_token = os.getenv('GITLAB_PRIVATE_TOKEN')

# Initialize the GitLab connection
gl = gitlab.Gitlab('https://gitlab.com', private_token=private_token)

# Function to get the commits for a specific date and project
def get_commits_for_date(project, date_str):
    start_date = f'{date_str}T00:00:00Z'
    end_date = f'{date_str}T23:59:59Z'
    commits = project.commits.list(since=start_date, until=end_date, all=True)
    if commits:
        return commits[0], commits[-1]  # first and last commit of the day
    return None, None

# Set the date range for the past 2 years
end_date = datetime.now()
start_date = end_date - timedelta(days=2*365)

commit_history = []

# Iterate over all projects the user has access to
for project in gl.projects.list(all=True):
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        first_commit, last_commit = get_commits_for_date(project, date_str)
        if first_commit and last_commit:
            commit_history.append({
                'Project': project.name,
                'Date': date_str,
                'First Commit ID': first_commit.id,
                'First Commit Message': first_commit.message,
                'Last Commit ID': last_commit.id,
                'Last Commit Message': last_commit.message
            })
        current_date += timedelta(days=1)

# Create a DataFrame and save to Excel
df = pd.DataFrame(commit_history)
df.to_excel('commit_history.xlsx', index=False)

print("Commit history has been saved to 'commit_history.xlsx'")
