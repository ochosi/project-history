# Project History Generator

This repository contains tools for generating comprehensive project histories from Git repositories, supporting GitHub, GitLab, and Jira.

## Repository Overview

**Purpose**: Automated tools + AI-assisted workflow for creating comprehensive project histories

**Key Scripts**:
- `fetch-github-history` - Fetch GitHub issues and pull requests
- `fetch-gitlab-history` - Fetch GitLab issues and merge requests
- `fetch-jira-history` - Fetch Jira tickets
- `fetch-history` - Unified script to fetch from all configured platforms
- `generate-history-draft` - Analyze git history and correlate with issues/PRs/tickets
- `setup-project` - Interactive configuration for new projects

## When This Repository Is Opened

When a user opens this repository in Claude Code, they are likely trying to:

1. **Use these tools on another project**: They want to copy these tools to their project and generate its history
2. **Configure the tools**: They need to set up authentication tokens and project information
3. **Run the history generation workflow**: They want to follow the complete workflow documented in `HISTORY_GENERATION_GUIDE.md`

## Typical User Workflow

### First-Time Setup
1. The user should run `./tools/setup-project` from the project root to configure:
   - Git remote (auto-detected from git or manually specified)
   - Platform (GitHub, GitLab, or both)
   - Jira integration (optional)
   - Authentication tokens via environment variables

2. Set environment variables for authentication:
   ```bash
   export GITHUB_TOKEN="ghp_..."      # For GitHub
   export GITLAB_TOKEN="glpat-..."    # For GitLab
   export JIRA_TOKEN="..."            # For Jira
   export JIRA_EMAIL="user@co.com"   # For Atlassian Cloud (*.atlassian.net)
   export JIRA_URL="https://..."      # Jira instance URL
   export JIRA_PROJECT="PROJ"         # Jira project key
   ```

### Running History Generation
1. Fetch data from all configured platforms:
   ```bash
   ./fetch-history
   ```

2. Generate timeline and analysis:
   ```bash
   ./generate-history-draft
   ```

3. Follow the AI-assisted curation workflow in `HISTORY_GENERATION_GUIDE.md`

## Configuration

The project configuration is stored in `.project-history-config.json` (created by `setup-project`).

### Configuration Schema
```json
{
  "platforms": {
    "github": {
      "enabled": true,
      "owner": "owner-name",
      "repo": "repo-name"
    },
    "gitlab": {
      "enabled": false,
      "project_id": "namespace/project",
      "url": "https://gitlab.com"
    },
    "jira": {
      "enabled": false,
      "url": "https://company.atlassian.net",
      "project_key": "PROJ"
    }
  },
  "output_dir": "./history"
}
```

## Authentication

All authentication is done via environment variables (never committed to git):

- **GitHub**: `GITHUB_TOKEN` - Create at https://github.com/settings/tokens (needs `repo` scope)
- **GitLab**: `GITLAB_TOKEN` - Create at GitLab Settings → Access Tokens (needs `read_api` scope)
- **Jira**: `JIRA_TOKEN` - Create at Jira Account Settings → Security → API tokens

## Common Tasks

### When the user asks to "set up this project":
1. Run `./setup-project` to configure platforms
2. Guide them to create authentication tokens
3. Help them set environment variables

### When the user asks to "generate history":
1. Verify configuration exists (`.project-history-config.json`)
2. Verify environment variables are set
3. Run `./fetch-history` followed by `./generate-history-draft`
4. Point them to `HISTORY_GENERATION_GUIDE.md` for the curation workflow

### When the user asks to "copy these tools to my project":
1. Copy only the scripts and guide to their project's `tools/` directory:
   `fetch-history`, `fetch-github-history`, `fetch-gitlab-history`,
   `fetch-jira-history`, `generate-history-draft`, `setup-project`,
   and `HISTORY_GENERATION_GUIDE.md`.
   Do NOT copy `CLAUDE.md`, `README.md`, `.git/`, `tests/`, or other repo files.
2. Run `./tools/setup-project` from the project root
3. Guide them through the complete workflow

## Important Notes

- **Never commit tokens**: All authentication uses environment variables
- **Git remote auto-detection**: Scripts can detect GitHub/GitLab from `git remote get-url origin`
- **Resumable processing**: `generate-history-draft` saves state and can resume if interrupted
- **Multi-platform correlation**: The generator correlates commits with PRs, MRs, and Jira tickets

## File Structure

After running the tools, the `history/` directory will contain:
```
history/
├── metadata.json              # GitHub stats
├── metadata-gitlab.json       # GitLab stats
├── metadata-jira.json         # Jira stats
├── issues/                    # GitHub issues
│   ├── open/
│   └── closed/
├── pull-requests/             # GitHub PRs
│   ├── open/
│   ├── merged/
│   └── closed/
├── merge-requests/            # GitLab MRs
│   ├── opened/
│   ├── merged/
│   └── closed/
├── jira-issues/               # Jira tickets
│   ├── open/
│   ├── done/
│   └── [other-statuses]/
└── draft/                     # Generated analysis
    ├── data/
    │   ├── correlation.json
    │   ├── important_prs.json
    │   └── theme_analysis.json
    ├── timeline/
    │   └── [period].md
    └── narrative/
        └── [period].md
```

## Troubleshooting

### "Repository not configured"
- Run `./setup-project` to create configuration

### "Token not set"
- Set the appropriate environment variable (GITHUB_TOKEN, GITLAB_TOKEN, or JIRA_TOKEN)

### "Could not detect git remote"
- Manually specify repository in setup or via command-line arguments

### "Rate limit exceeded"
- Scripts handle rate limits automatically with backoff
- For GitHub, use a different token or wait for limit reset

## For Claude Code Users

When helping users with this repository:

1. **Always check if `.project-history-config.json` exists** - if not, suggest running `./setup-project`
2. **Verify environment variables** - remind users to set tokens before fetching
3. **Guide through the workflow** - reference `HISTORY_GENERATION_GUIDE.md` for the complete process
4. **Multi-platform support** - ask which platforms they use (GitHub, GitLab, Jira, or combination)
5. **Be proactive about setup** - if they mention generating history, ensure configuration is complete first
