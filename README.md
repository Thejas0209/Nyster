# Nyster

Nyster is a powerful integration tool that allows seamless interaction with GitHub and GitLab through a set of easy-to-use commands. This guide will help you get started and use all the commands available for managing your GitHub and GitLab repositories efficiently.

---

## Getting Started

### 1. Clone the Repository

Follow these steps to clone the GitHub repository to your local storage:

```bash
# Open Terminal
# Navigate to the directory where you want to store the project
cd /path/to/your/directory

# Clone the repository
git clone https://github.com/Thejas0209/Nyster.git
```

---

### 2. Setting Up the `.env` File

This project requires specific environment variables to be configured in a `.env` file for proper functionality. Follow the steps below:

```bash
# Step 1: Create a .env file in the root directory of the project
type nul > .env

# Step 2: Open the .env file and add the required variables
# Use the format KEY=VALUE (no spaces around the = sign)
```

#### Example `.env` File:

```env
# Discord Bot Token
DISCORD_TOKEN=your_discord_token_here

# MongoDB Connection URL
MONGO_DB_URL=your_mongo_db_connection_url_here

# GitHub Database Name
GITHUB_DB=your_github_database_name_here

# Table Names
TABLE_USERS=your_userinfo_table_name_here
TABLE_RELEASES_TRACKERS=your_releases_trackers_table_name_here
TABLE_COMMITS_TRACKERS=your_commits_trackers_table_name_here

# GitLab Database Name
GITLAB_DB=your_gitlab_database_name_here
```

---

### 3. GitHub and GitLab Token Setup

To enable Nyster’s integration with GitHub and GitLab, set up your tokens as follows:

#### GitHub Setup

```bash
# Run the /github-setup command and provide your GitHub token
# Ensure that the token has read-only access for enhanced security
```

#### GitLab Setup

```bash
# Run the /gitlab-setup command and provide your GitLab token
# Ensure that the token has read-only access for enhanced security
```

---

## Available Commands

### GitHub Commands

Use these commands to manage and interact with GitHub repositories:

```bash
# 1. /github-setup
# Description: Set up your GitHub token
# Usage: Run this command and input your GitHub token to enable access

# 2. /github-setup-remove
# Description: Remove your GitHub token
# Usage: Disconnect your GitHub integration

# 3. /github-status
# Description: Check the status of your GitHub integration
# Usage: Confirm if your GitHub token is configured correctly

# 4. /github-commits
# Description: Fetch the latest commits from a specified repository
# Usage: Provides recent commit information for a given GitHub repository

# 5. /github-repo-info
# Description: Display detailed information about a specific GitHub repository
# Usage: Retrieve information such as the owner, description, and stats of the repository

# 6. /github-track-commits
# Description: Start tracking commits from a repository and receive notifications
# Usage: Enable notifications for new commits

# 7. /github-untrack-commits
# Description: Stop tracking commits for a repository
# Usage: Disable notifications for new commits

# 8. /github-track-releases
# Description: Start tracking new releases of a repository
# Usage: Get notified when a new release is published

# 9. /github-untrack-releases
# Description: Stop tracking releases of a repository
# Usage: Disable notifications for new releases
```

### GitLab Commands

Use these commands to manage and interact with GitLab repositories:

```bash
# 1. /gitlab-setup
# Description: Set up your GitLab token
# Usage: Run this command and input your GitLab token to enable access

# 2. /gitlab-setup-remove
# Description: Remove your GitLab token
# Usage: Disconnect your GitLab integration

# 3. /gitlab-status
# Description: Check the status of your GitLab integration
# Usage: Confirm if your GitLab token is configured correctly

# 4. /gitlab-repo-info
# Description: Display detailed information about a specific GitLab repository
# Usage: Retrieve general information such as the owner, description, and stats of the repository
```

---

This guide provides an overview of the commands and their functionalities. Ensure that you have the appropriate permissions set for your tokens, and use these commands to effectively manage your repositories.
```

