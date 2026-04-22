# Project History Generator

**Automated tools + AI-assisted workflow for creating comprehensive project histories from Git repositories**

This repository contains everything you need to generate a detailed, human-readable history of any project, supporting **GitHub**, **GitLab**, and **Jira** integration.

## What This Does

Transforms raw git history and issue tracking data into narrative documentation:

- **Input**: Any Git repository with GitHub, GitLab, or both, plus optional Jira integration
- **Output**: Comprehensive historical narratives organized by time period
- **Process**: Automated data collection + AI-assisted analysis and writing
- **Time**: ~30-48 hours of focused work for a mature multi-year project

## What's Included

- `setup-project` - Interactive configuration wizard for new projects
- `fetch-github-history` - Fetch all GitHub issues and PRs as markdown
- `fetch-gitlab-history` - Fetch all GitLab issues and merge requests as markdown
- `fetch-jira-history` - Fetch all Jira tickets as markdown
- `fetch-history` - Unified script to fetch from all configured platforms
- `generate-history-draft` - Analyze git history and correlate with issues/PRs/MRs/tickets
- `HISTORY_GENERATION_GUIDE.md` - Complete workflow with proven AI prompts
- `CLAUDE.md` - Context for Claude Code users

## Platform Support

This tooling supports multiple platforms simultaneously:

| Platform | What's Fetched | Reference Format | Required Token |
|----------|----------------|------------------|----------------|
| **GitHub** | Issues, Pull Requests, Reviews, Comments | `#123` | `GITHUB_TOKEN` |
| **GitLab** | Issues, Merge Requests, Notes | `!123` | `GITLAB_TOKEN` |
| **Jira** | Issues/Tickets, Comments | `PROJ-123` | `JIRA_TOKEN` |

**Multi-platform projects**: You can enable any combination of platforms. For example:
- GitHub for code hosting + Jira for project management
- GitLab for everything (code + issues)
- GitHub + GitLab (for projects that migrated between platforms)

The `generate-history-draft` script automatically correlates git commits with references to PRs, MRs, and Jira tickets, creating a unified timeline.

## Quick Start

### Prerequisites

1. **Python 3.8+** with `requests` library:
   ```bash
   pip install requests
   ```

2. **Authentication Tokens** (for the platforms you use):

   **GitHub** - Personal Access Token with `repo` scope:
   - Go to: https://github.com/settings/tokens
   - Generate new token (classic)
   - Select scope: `repo` (Full control of private repositories)

   **GitLab** - Personal Access Token with `read_api` scope:
   - Go to: GitLab Settings → Access Tokens
   - Create token with `read_api` scope

   **Jira** - API Token:
   - Go to: Jira Account Settings → Security → API Tokens
   - Create API token

3. **AI Assistant** (Claude Code or Cursor):
   - This workflow is designed for AI pair programming
   - You'll use the AI to analyze data and write narratives

### Using with Claude Code

1. **Copy the scripts into your project**:
   ```bash
   cd /path/to/your-project
   mkdir -p ./tools
   cp /path/to/project-history/fetch-* \
      /path/to/project-history/generate-history-draft \
      /path/to/project-history/setup-project \
      /path/to/project-history/HISTORY_GENERATION_GUIDE.md \
      ./tools/
   ```
   Do **not** copy `CLAUDE.md`, `README.md`, `.git/`, `tests/`, or other
   repo files — they belong to the project-history repo and will confuse
   tools if present in your project.

2. **Run the interactive setup**:
   ```bash
   ./tools/setup-project
   ```
   This creates `.project-history-config.json` in your project root and
   asks about:
   - Git hosting platform (GitHub, GitLab, or both)
   - Project identifiers (auto-detected from git remote if possible)
   - Jira integration (optional)

3. **Set up your authentication tokens**:
   ```bash
   export GITHUB_TOKEN="your_github_token_here"    # If using GitHub
   export GITLAB_TOKEN="your_gitlab_token_here"    # If using GitLab
   export JIRA_TOKEN="your_jira_token_here"        # If using Jira
   export JIRA_EMAIL="your_email@company.com"      # If using Atlassian Cloud
   ```

4. **Start Claude Code and begin the workflow**:
   ```bash
   claude
   ```
   Then give Claude this prompt:
   ```
   I want to generate a comprehensive history of this project.
   Please follow the workflow in tools/HISTORY_GENERATION_GUIDE.md.

   Start with Phase 1: Data Collection
   ```

5. **Let Claude guide you through each phase**:
   - Phase 1: Automated data fetching (Claude runs the scripts)
   - Phase 2-5: AI-assisted curation and writing (you collaborate with Claude)

### Using with Cursor

1. **Open your target repository** in Cursor:
   ```bash
   cd /path/to/your-project
   cursor .
   ```

2. **Copy the scripts** using Cursor's file explorer or terminal:
   ```bash
   mkdir -p ./tools
   cp /path/to/project-history/fetch-* \
      /path/to/project-history/generate-history-draft \
      /path/to/project-history/setup-project \
      /path/to/project-history/HISTORY_GENERATION_GUIDE.md \
      ./tools/
   ```
   Do **not** copy `CLAUDE.md`, `README.md`, `.git/`, `tests/`, or other repo files.

3. **Set your GitHub token** in Cursor's terminal:
   ```bash
   export GITHUB_TOKEN="your_github_token_here"
   ```

4. **Open `tools/HISTORY_GENERATION_GUIDE.md`** in Cursor

5. **Use Cursor's AI chat** to work through each phase:
   - Copy each numbered prompt from the guide
   - Paste into Cursor chat
   - Review and refine Claude's output

## Workflow Overview

### Phase 1: Data Collection (Day 1)
Run the automation scripts to fetch all data:
```bash
# Fetch from all configured platforms (GitHub, GitLab, Jira)
./tools/fetch-history --verbose

# OR fetch individually:
./tools/fetch-github-history --verbose   # GitHub only
./tools/fetch-gitlab-history --verbose   # GitLab only
./tools/fetch-jira-history --verbose     # Jira only

# Generate correlation and timeline data  
./tools/generate-history-draft --verbose
```

**Output**: `history/` directory with issues, PRs, MRs, Jira tickets, timelines, and analysis data

### Phase 2: Curation (Days 2-3)
Use AI prompts to identify:
- Top 20-30 most significant PRs
- Key contributors and their areas
- Project phases and inflection points

### Phase 3: Deep Dives (Days 3-4)
Research each significant PR in detail:
- Read PR discussions
- Analyze linked issues
- Understand the decision-making process

### Phase 4: Narrative Writing (Days 4-6)
Write comprehensive narratives:
- One document per time period (e.g., genesis, foundation, maturation)
- Main PROJECT_HISTORY.md overview
- Focus on "why" not just "what"

### Phase 5: Validation (Day 6-7)
Validate and polish:
- Verify all facts and attributions
- Ensure consistency
- Fix any errors

**See `HISTORY_GENERATION_GUIDE.md` for detailed prompts at each step.**

## Example Prompts for AI Chat

### Starting the Process
```
I want to generate a comprehensive project history. I've copied the 
scripts from project-history into my tools/ directory. Please help me:

1. Run ./tools/setup-project to configure my project
2. Run ./tools/fetch-history to get all data from GitHub/GitLab/Jira
3. Run ./tools/generate-history-draft to analyze git history
4. Then guide me through the curation process using the prompts in 
   tools/HISTORY_GENERATION_GUIDE.md
```

### Curation Phase
```
Please analyze history/draft/data/important_prs.json and identify 
the top 20 most architecturally significant PRs. For each, explain:
- Why it's significant
- What changed
- Any breaking changes

Use the "Prompt 1" format from HISTORY_GENERATION_GUIDE.md
```

### Writing Phase
```
Write a comprehensive narrative for the "Foundation" period 
(2019-07-01 to 2020-12-31) using the resources in:
- history/draft/timeline/foundation.md
- history/draft/deep-dives/
- history/draft/curated/

Follow the structure from "Prompt 6" in HISTORY_GENERATION_GUIDE.md
```

## Customization

### Adjust Time Periods

Edit `generate-history-draft` around line 406:

```python
PERIODS = {
    'early': {
        'start': '2018-01-01',
        'end': '2019-12-31',
        'description': 'Initial development'
    },
    'growth': {
        'start': '2020-01-01',
        'end': '2022-12-31',
        'description': 'Production adoption'
    },
    # Add periods that match your project
}
```

### Adjust Themes

Edit `generate-history-draft` around line 260:

```python
THEMES = {
    'api': {
        'keywords': ['api', 'endpoint', 'rest', 'graphql'],
        'description': 'API changes'
    },
    'performance': {
        'keywords': ['perf', 'optimization', 'cache', 'speed'],
        'description': 'Performance improvements'
    },
    # Add themes relevant to your project
}
```

## Example: Typical AI Chat Session

```
You: I want to create a history of this project following the guide 
in tools/HISTORY_GENERATION_GUIDE.md. Let's start with Phase 1.

Claude: I'll help you generate a comprehensive project history. 
Let's start by fetching the GitHub data...

[Claude runs fetch-github-history]

Claude: Successfully fetched 156 issues and 892 PRs. Now analyzing 
git history...

[Claude runs generate-history-draft]

Claude: Analysis complete. I've identified 267 important PRs and 
generated timelines for 4 periods. Let's move to Phase 2: Curation.

Looking at the important_prs.json, here are the top 20 most 
significant PRs...

You: Great! For PR #45, can you do a deep dive analysis?

Claude: [Reads PR file, related commits, and linked issues]

Here's my analysis of PR #45:

**Problem**: The original authentication system stored passwords 
in plaintext...

[etc.]
```

## Output Structure

After completion, your project will have:

```
your-project/
├── .project-history-config.json    ← Configuration file
├── tools/
│   ├── setup-project
│   ├── fetch-history
│   ├── fetch-github-history
│   ├── fetch-gitlab-history
│   ├── fetch-jira-history
│   ├── generate-history-draft
│   └── HISTORY_GENERATION_GUIDE.md
└── history/
    ├── PROJECT_HISTORY.md          ← Main entry point
    ├── metadata.json               ← GitHub stats
    ├── metadata-gitlab.json        ← GitLab stats
    ├── metadata-jira.json          ← Jira stats
    ├── issues/                     ← GitHub issues
    │   ├── open/
    │   └── closed/
    ├── pull-requests/              ← GitHub PRs
    │   ├── open/
    │   ├── merged/
    │   └── closed/
    ├── merge-requests/             ← GitLab MRs
    │   ├── opened/
    │   ├── merged/
    │   └── closed/
    ├── jira-issues/                ← Jira tickets
    │   ├── open/
    │   ├── done/
    │   └── [other-statuses]/
    └── draft/
        ├── narrative/              ← Period narratives
        ├── curated/                ← Curated analysis
        ├── deep-dives/             ← PR/MR analyses
        ├── timeline/               ← Auto-generated timelines
        └── data/                   ← Machine-readable data
            ├── correlation.json
            ├── important_prs.json
            ├── important_mrs.json
            ├── jira_references.json
            └── theme_analysis.json
```

## Tips for Best Results

### Do's
- ✅ Read the full HISTORY_GENERATION_GUIDE.md before starting
- ✅ Use the provided prompts - they're proven to work well
- ✅ Validate contributor attributions carefully
- ✅ Quote from actual PR discussions
- ✅ Focus on "why" decisions were made, not just "what" happened
- ✅ Be honest about mistakes and pivots

### Don'ts  
- ❌ Don't skip the validation phase
- ❌ Don't write marketing copy - keep it technical
- ❌ Don't try to cover every single commit
- ❌ Don't assume - verify facts against actual PRs/issues
- ❌ Don't rush - good history takes time

## Real-World Examples

This tooling has been used to create comprehensive project histories for various projects:

**Multi-year projects**:
- **7+ years of history** analyzed
- **4,000+ commits** processed
- **2,000+ PRs/MRs** correlated
- **6+ period narratives** written
- **~15,000 words** of documentation

The resulting histories document architectural evolution, key contributors, design decisions, and the reasoning behind major technical choices.

**Multi-platform projects**:
- Combined GitHub PR and Jira ticket correlation
- GitLab-hosted projects with issue tracking
- Hybrid setups with multiple platforms

## Troubleshooting

### "Configuration file not found"
Run `./setup-project` to create the configuration:
```bash
./setup-project
```

### "Token not set"
Set the appropriate environment variable(s):
```bash
export GITHUB_TOKEN="ghp_your_token_here"     # For GitHub
export GITLAB_TOKEN="glpat-your_token_here"   # For GitLab
export JIRA_TOKEN="your_token_here"           # For Jira
```

### "Rate limit exceeded"
The fetch scripts handle rate limits automatically. If you hit limits:
- Wait for the cooldown period (script will show countdown)
- Or use a different token

### "Not a git repository"
Make sure you run the scripts from your project's git repository root.

### "Could not detect git remote"
If auto-detection fails, manually specify your repository during setup or use command-line arguments:
```bash
./fetch-github-history --repo owner/repo
./fetch-gitlab-history --project namespace/project --gitlab-url https://gitlab.com
```

### Scripts not executable
```bash
chmod +x setup-project fetch-history fetch-github-history fetch-gitlab-history fetch-jira-history generate-history-draft
```

## Contributing

This is a standalone tooling repository. If you improve the scripts or workflow:

1. Test on multiple project types
2. Document what you changed and why
3. Share improvements with others who use this

## License

These tools are provided as-is for generating project documentation. Use freely for any project.

## Questions?

The tools are self-contained and the guide includes everything needed. If you get stuck:
1. Re-read the relevant section in HISTORY_GENERATION_GUIDE.md
2. Ask your AI assistant to explain the prompt
3. Check the example outputs in the guide

Good luck documenting your project's history!
