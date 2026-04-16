# Project History Generator

**Automated tools + AI-assisted workflow for creating comprehensive project histories from GitHub repositories**

This repository contains everything you need to generate a detailed, human-readable history of any GitHub project, documenting its evolution, key decisions, and contributor stories.

## What This Does

Transforms raw git/GitHub data into narrative documentation:

- **Input**: Any GitHub repository with git history
- **Output**: Comprehensive historical narratives organized by time period
- **Process**: Automated data collection + AI-assisted analysis and writing
- **Time**: ~30-48 hours of focused work for a mature multi-year project

## What's Included

- `fetch-github-history` - Python script to fetch all GitHub issues and PRs as markdown
- `generate-history-draft` - Python script to analyze git history and generate timelines
- `HISTORY_GENERATION_GUIDE.md` - Complete workflow with proven AI prompts

## Quick Start

### Prerequisites

1. **Python 3.8+** with `requests` library:
   ```bash
   pip install requests
   ```

2. **GitHub Personal Access Token** with `repo` scope:
   - Go to: https://github.com/settings/tokens
   - Generate new token (classic)
   - Select scope: `repo` (Full control of private repositories)
   - Copy the token

3. **AI Assistant** (Claude Code or Cursor):
   - This workflow is designed for AI pair programming
   - You'll use the AI to analyze data and write narratives

### Using with Claude Code

1. **Open your target repository** in Claude Code:
   ```bash
   cd /path/to/your-project
   claude
   ```

2. **Copy this repository's scripts into your project**:
   ```bash
   # From Claude Code chat:
   "Please copy the scripts from /path/to/project-history/ into a tools/ directory in this project"
   ```

3. **Set up your environment**:
   ```bash
   export GITHUB_TOKEN="your_github_token_here"
   ```

4. **Start the workflow**:
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
   mkdir tools
   cp /path/to/project-history/* tools/
   ```

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
# Fetch all GitHub data
./tools/fetch-github-history --verbose

# Generate correlation and timeline data  
./tools/generate-history-draft --verbose
```

**Output**: `history/` directory with issues, PRs, timelines, and analysis data

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

1. Run ./tools/fetch-github-history to get all GitHub data
2. Run ./tools/generate-history-draft to analyze git history
3. Then guide me through the curation process using the prompts in 
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
├── tools/
│   ├── fetch-github-history
│   ├── generate-history-draft
│   └── HISTORY_GENERATION_GUIDE.md
└── history/
    ├── PROJECT_HISTORY.md          ← Main entry point
    ├── issues/                      ← All GitHub issues
    ├── pull-requests/               ← All GitHub PRs
    └── draft/
        ├── narrative/               ← Period narratives
        ├── curated/                 ← Curated analysis
        ├── deep-dives/              ← PR analyses
        ├── timeline/                ← Auto-generated timelines
        └── data/                    ← Machine-readable data
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

## Real-World Example

This tooling was used to create the comprehensive history of the **osbuild project**:
- **7 years of history** (2019-2026)
- **4,105 commits** analyzed
- **2,104 PRs** processed
- **6 period narratives** written
- **~15,000 words** of documentation

The resulting history documents architectural evolution, key contributors, and design decisions that shaped the project.

## Troubleshooting

### "Rate limit exceeded"
The `fetch-github-history` script handles rate limits automatically. If you hit limits:
- Wait for the cooldown period (script will show countdown)
- Or use a different GitHub token

### "Not a git repository"
Make sure you run the scripts from your project's git repository root.

### "GITHUB_TOKEN not set"
```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

### Scripts not executable
```bash
chmod +x fetch-github-history generate-history-draft
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
