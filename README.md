# Nyster

Nyster is a powerful integration tool that allows seamless interaction with GitHub and GitLab through a set of easy-to-use commands. This guide will help you get started and understand all the commands available for managing your GitHub and GitLab repositories.

## Getting Started

Before using the commands, you need to set up your GitHub and GitLab tokens:

### GitHub Setup
1. Run the `/github-setup` command and provide your GitHub token.
2. Ensure that the token has **read-only access** for security and limited functionality.

### GitLab Setup
1. Run the `/gitlab-setup` command and provide your GitLab token.
2. Ensure that the token has **read-only access** for security and limited functionality.

## Available Commands

### GitHub Commands
These commands help you manage and interact with GitHub repositories:

1. **`/github-setup`**
   - **Description**: Set up your GitHub token.
   - **Usage**: Run this command and input your GitHub token to enable access.
2. **`/github-setup-remove`**
   - **Description**: Remove your GitHub token.
   - **Usage**: Use this command to disconnect your GitHub integration.
3. **`/github-status`**
   - **Description**: Check the status of your GitHub integration.
   - **Usage**: Confirm if your GitHub token is configured correctly.
4. **`/github-commits`**
   - **Description**: Fetch the latest commits from a specified repository.
   - **Usage**: Provides recent commit information for a given GitHub repository.
5. **`/github-repo-info`**
   - **Description**: Display detailed information about a specific GitHub repository.
   - **Usage**: Retrieve general information such as the owner, description, and stats of the repository.
6. **`/github-track-commits`**
   - **Description**: Start tracking commits from a repository and receive notifications.
   - **Usage**: Enable notifications for new commits.
7. **`/github-untrack-commits`**
   - **Description**: Stop tracking commits of a repository.
   - **Usage**: Disable notifications for new commits.
8. **`/github-track-releases`**
   - **Description**: Start tracking new releases of a repository.
   - **Usage**: Get notified when a new release is published.
9. **`/github-untrack-releases`**
   - **Description**: Stop tracking releases of a repository.
   - **Usage**: Disable notifications for new releases.

### GitLab Commands
These commands help you manage and interact with GitLab repositories:

1. **`/gitlab-setup`**
   - **Description**: Set up your GitLab token.
   - **Usage**: Run this command and input your GitLab token to enable access.
2. **`/gitlab-setup-remove`**
   - **Description**: Remove your GitLab token.
   - **Usage**: Use this command to disconnect your GitLab integration.
3. **`/gitlab-status`**
   - **Description**: Check the status of your GitLab integration.
   - **Usage**: Confirm if your GitLab token is configured correctly.
4. **`/gitlab-repo-info`**
   - **Description**: Display detailed information about a specific GitLab repository.
   - **Usage**: Retrieve general information such as the owner, description, and stats of the repository.

---

This guide provides an overview of the commands and their functionalities. Ensure that you have the appropriate permissions set for your tokens, and use these commands to effectively manage your repositories.
