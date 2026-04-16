# Project History Generation Guide

This guide provides a complete workflow for generating comprehensive project histories from Git repositories using automated tools and AI-assisted narrative writing.

## Overview

The history generation process combines:
- **Automated data fetching** from GitHub/GitLab/Jira (issues, PRs, MRs, tickets, metadata)
- **Git analysis** to correlate commits with PRs/MRs/tickets and detect themes
- **AI-assisted synthesis** to write human-readable narratives

**Time estimate**: 5-7 days for a multi-year project with 2,000+ PRs/MRs

## Prerequisites

### Required Tools
- Python 3.8+
- Git
- Authentication tokens for your platforms (see below)
- AI assistant with file access (Claude, GPT-4, etc.)

### Required Scripts
All scripts are included in this directory:
- `setup-project` - Interactive configuration wizard
- `fetch-history` - Unified fetcher for all platforms
- `fetch-github-history` - Fetches GitHub data as markdown
- `fetch-gitlab-history` - Fetches GitLab data as markdown
- `fetch-jira-history` - Fetches Jira data as markdown
- `generate-history-draft` - Analyzes git history and creates timelines

### Setup
```bash
# Install Python dependencies
pip install requests

# Run interactive setup
./setup-project

# Set your authentication tokens (as prompted by setup-project)
export GITHUB_TOKEN="your_github_token_here"    # If using GitHub
export GITLAB_TOKEN="your_gitlab_token_here"    # If using GitLab
export JIRA_TOKEN="your_jira_token_here"        # If using Jira

# Make scripts executable
chmod +x setup-project fetch-history fetch-github-history fetch-gitlab-history fetch-jira-history generate-history-draft
```

## Workflow

### Phase 1: Data Collection (Day 1)

#### Step 1: Fetch Platform Data

```bash
# From your repository root
# Fetch from all configured platforms
./tools/fetch-history --verbose

# OR fetch individually:
./tools/fetch-github-history --verbose   # GitHub only
./tools/fetch-gitlab-history --verbose   # GitLab only
./tools/fetch-jira-history --verbose     # Jira only
```

This creates:
- `history/issues/` - GitHub issues organized by state
- `history/pull-requests/` - GitHub PRs organized by state (open/closed/merged)
- `history/merge-requests/` - GitLab MRs organized by state (opened/closed/merged)
- `history/jira-issues/` - Jira tickets organized by status
- `history/metadata*.json` - Summary statistics for each platform

**Expected output**: 
- Issues: ~100-500 for typical projects
- PRs/MRs: ~500-5,000 for mature projects
- Jira tickets: ~50-1,000 depending on usage
- Time: 5-30 minutes depending on size and platforms

#### Step 2: Generate Analysis Data

```bash
# Generate correlation and timeline data
./tools/generate-history-draft --verbose
```

This creates:
- `history/draft/data/correlation.json` - Commit→PR/MR/Jira mappings
- `history/draft/data/important_prs.json` - High-impact GitHub PRs (scored)
- `history/draft/data/important_mrs.json` - High-impact GitLab MRs (scored)
- `history/draft/data/jira_references.json` - Referenced Jira tickets
- `history/draft/data/theme_analysis.json` - Categorized changes
- `history/draft/timeline/*.md` - Timeline files by period

**Note**: The script uses predefined time periods. Edit `generate-history-draft` to customize:
```python
PERIODS = {
    'early': {'start': '2019-01-01', 'end': '2020-12-31'},
    'growth': {'start': '2021-01-01', 'end': '2022-12-31'},
    # ... customize for your project
}
```

### Phase 2: Curation (Days 2-3)

Now use your AI assistant to identify the most important changes. Here are proven prompts:

#### Prompt 1: Identify Architectural Milestones

```
I have generated history data for [PROJECT_NAME]. Please analyze the following files:
- history/draft/data/important_prs.json (GitHub PRs)
- history/draft/data/important_mrs.json (GitLab MRs, if available)
- history/draft/data/jira_references.json (Jira tickets, if available)
- history/draft/data/theme_analysis.json
- history/draft/timeline/*.md

Identify the top 20-30 most architecturally significant changes (PRs, MRs, or major commits). 
For each, note:
1. Reference number (PR#, MR!, or Jira key) and title
2. Why it's architecturally significant
3. What changed in the codebase
4. Any breaking changes or migrations

Focus on:
- Core architecture changes (data models, APIs, file formats)
- Isolation/execution model changes
- Major feature additions that shaped the project
- Breaking changes that required migrations
- Performance or scalability improvements

Save this as history/draft/curated/architectural_milestones.md
```

#### Prompt 2: Identify Key Contributors

```
Please analyze the git commit history and GitHub data to identify:

1. Top 10-15 contributors by:
   - Commit count
   - High-impact PRs authored
   - Code review participation
   
2. For each contributor:
   - GitHub username
   - Real name (if available in git commits or PR metadata)
   - Their primary areas of contribution (use theme_analysis.json)
   - Time period when they were most active
   
3. Special roles:
   - Project founders (first 5 commits)
   - Maintainers (frequent reviewers)
   - Domain experts (concentrated in specific themes)

Save as history/draft/curated/key_contributors.md
```

#### Prompt 3: Detect Evolution Patterns

```
Review the timeline files in history/draft/timeline/ and identify:

1. **Phases of development**: 
   - When did the project start?
   - When did it move from prototype to production?
   - When did major architectural shifts happen?
   - When did community grow significantly?

2. **Recurring themes**:
   - What types of changes happen most frequently?
   - Are there seasonal patterns (e.g., more features in Q1, more fixes in Q4)?
   - How has the focus shifted over time?

3. **Inflection points**:
   - Sudden increases in activity
   - Major refactorings
   - Introduction of new subsystems

Propose a period structure (3-6 periods) that captures the project's evolution.
Save as history/draft/curated/period_structure.md
```

### Phase 3: Deep Dives (Days 3-4)

For each architectural milestone identified, conduct deep research:

#### Prompt 4: Research Significant PR

```
Please research PR #[NUMBER] in detail:

1. Read the PR markdown file at: history/pull-requests/merged/[NUMBER]-*.md

2. Find related commits:
   - Search history/draft/data/correlation.json for this PR number
   - Read commit messages for context

3. Check if there are linked issues:
   - Look for "fixes #X" or "closes #X" in the PR description
   - Read those issue files

4. Analyze the discussion:
   - What problem was being solved?
   - What alternatives were considered?
   - What concerns were raised in review?
   - What was the final decision and why?

5. Write a 200-300 word summary covering:
   - The problem/motivation
   - The solution approach
   - Key design decisions
   - Impact on the project
   - Notable quote from the discussion (if any)

Save as history/draft/deep-dives/pr-[NUMBER]-analysis.md
```

Repeat for each of your top 20-30 PRs.

#### Prompt 5: Validate Contributor Attribution

```
I've created a list of key contributors. Please validate the GitHub username → real name mappings:

1. For each contributor, check:
   - Git commit author names (use: git log --format="%an <%ae>" --author="username" | head -5)
   - PR author fields in history/pull-requests/
   - Any @mentions in PR discussions

2. Flag any uncertainties or conflicts

3. Create a verified mapping file

Save as history/draft/curated/contributor_mapping.json in format:
{
  "github_username": {
    "name": "Real Name",
    "email": "email@domain.com",
    "confidence": "high|medium|low"
  }
}
```

### Phase 4: Narrative Writing (Days 4-6)

Now write the actual history narratives:

#### Prompt 6: Write Period Narrative

```
Write a comprehensive narrative for the [PERIOD_NAME] period ([START_DATE] to [END_DATE]).

Use these resources:
- Timeline: history/draft/timeline/[period].md
- Deep dives: history/draft/deep-dives/pr-*-analysis.md (for this period)
- Milestones: history/draft/curated/architectural_milestones.md
- Contributors: history/draft/curated/key_contributors.md

Structure:
1. **Opening** (1-2 paragraphs): What defined this period?
2. **Major themes** (3-5 sections): Group related changes
3. **Key milestones** (detailed): 
   - For top 3-5 PRs in the period, write 2-3 paragraphs each
   - Include PR numbers, contributor usernames, key quotes
4. **Impact** (1 paragraph): How did this period shape the project?

Style:
- Write for developers, not marketers
- Focus on "why" over "what"
- Include technical details
- Use contributor @usernames
- Quote from PR discussions when insightful
- Be honest about tradeoffs and mistakes

Length: 2,000-4,000 words

Save as history/draft/narrative/[period_name].md
```

Repeat for each period.

#### Prompt 7: Write Project Overview

```
Now that all period narratives are written, create the main PROJECT_HISTORY.md:

Structure:
1. **Executive Summary** (300-500 words)
   - What is this project?
   - Why does it exist?
   - How has it evolved?

2. **Timeline Overview** (table)
   - Period | Date Range | Key Theme | Major Milestones
   
3. **Period Summaries** (200 words each)
   - Brief overview of each period with links to full narratives

4. **Architectural Journey** (500-800 words)
   - How did core architecture evolve?
   - What were the major technical decisions?
   - Include a chronological list of breaking changes

5. **Community & Contributors** (300-500 words)
   - Key contributors with @usernames
   - Community growth over time
   - Collaboration patterns

6. **Lessons Learned** (300-500 words)
   - What worked well?
   - What would be done differently?
   - Insights for similar projects

Total length: 3,000-5,000 words

Save as history/PROJECT_HISTORY.md
```

### Phase 5: Validation & Refinement (Day 6-7)

#### Prompt 8: Validate Facts

```
Please validate the historical narratives for factual accuracy:

1. **Attribution verification**:
   - For each @username mentioned, verify they actually worked on what's claimed
   - Check git logs: git log --all --author="username" --oneline | wc -l
   - Check PR authorship in history/pull-requests/

2. **PR verification**:
   - For each PR mentioned, verify:
     - The PR number is correct
     - The description matches the actual PR
     - Quotes are accurate
   - Read the actual PR files

3. **Timeline verification**:
   - Ensure dates are correct
   - Verify order of events
   - Check that causality makes sense

4. **Technical accuracy**:
   - Verify technical claims against actual code/PRs
   - Flag any assumptions that need verification

Create a validation report listing:
- Confirmed facts
- Corrected errors
- Items needing maintainer review

Save as history/draft/validation_report.md
```

#### Prompt 9: Final Polish

```
Polish all narrative files for publication:

1. **Consistency**:
   - Ensure terminology is consistent across all documents
   - Standardize formatting (headings, lists, code blocks)
   - Use consistent @username format

2. **Readability**:
   - Add section breaks where needed
   - Ensure smooth transitions between sections
   - Verify all links work
   - Add a table of contents where appropriate

3. **Completeness**:
   - Every major PR mentioned should link to its file or GitHub
   - Every period should have a narrative
   - The main PROJECT_HISTORY.md should link to all period narratives

4. **Style**:
   - Remove any marketing language
   - Ensure technical accuracy
   - Keep tone professional but not dry

Update all files in place.
```

## Customization

### Adjusting Time Periods

Edit `generate-history-draft` line 406-437 to match your project:

```python
PERIODS = {
    'bootstrap': {
        'start': '2015-01-01',
        'end': '2016-12-31',
        'description': 'Initial development'
    },
    'production': {
        'start': '2017-01-01', 
        'end': '2019-12-31',
        'description': 'First production users'
    },
    # Add more periods as needed
}
```

### Adjusting Theme Detection

Edit `generate-history-draft` line 260-301 to match your project's themes:

```python
THEMES = {
    'api': {
        'keywords': ['api', 'endpoint', 'rest', 'graphql'],
        'description': 'API changes'
    },
    'database': {
        'keywords': ['migration', 'schema', 'sql', 'database'],
        'description': 'Database layer'
    },
    # Add themes relevant to your project
}
```

### Adjusting Importance Scoring

Edit `generate-history-draft` line 318-400 to tune what counts as "important":

```python
def score_pr(self, pr_data: Dict[str, Any]) -> int:
    score = 0
    
    # Customize these weights for your project
    if 'breaking-change' in labels:
        score += 20
    if 'rfc' in labels:
        score += 15
    # Add your own scoring criteria
    
    return min(score, 100)
```

## Output Structure

Your final `history/` directory should look like:

```
history/
├── PROJECT_HISTORY.md              # Main entry point
├── issues/                          # GitHub issues
│   ├── open/
│   └── closed/
├── pull-requests/                   # GitHub PRs
│   ├── merged/
│   ├── closed/
│   └── open/
├── draft/
│   ├── narrative/                   # Period narratives
│   │   ├── early.md
│   │   ├── growth.md
│   │   └── mature.md
│   ├── curated/                     # Curated analysis
│   │   ├── architectural_milestones.md
│   │   ├── key_contributors.md
│   │   └── contributor_mapping.json
│   ├── deep-dives/                  # PR analyses
│   │   ├── pr-0005-analysis.md
│   │   └── pr-0267-analysis.md
│   ├── timeline/                    # Auto-generated timelines
│   │   └── *.md
│   └── data/                        # Machine-readable data
│       ├── correlation.json
│       ├── important_prs.json
│       └── theme_analysis.json
└── metadata.json                    # Fetch metadata
```

## Tips & Best Practices

### Do's
- ✅ Start with high-impact PRs (breaking changes, architecture)
- ✅ Quote from PR discussions to capture decision-making
- ✅ Credit contributors with @usernames consistently  
- ✅ Link to actual PRs/issues for verification
- ✅ Be honest about mistakes and pivots
- ✅ Focus on "why" not just "what"
- ✅ Validate attribution carefully

### Don'ts
- ❌ Don't write marketing copy - this is technical history
- ❌ Don't assume correlation = causation in commit/PR matching
- ❌ Don't skip validation - incorrect attribution damages trust
- ❌ Don't try to cover every commit - focus on the significant ones
- ❌ Don't ignore the boring parts (infrastructure, testing, CI)
- ❌ Don't just list features - explain the problems being solved

### Common Pitfalls

1. **Attribution errors**: Always verify @username mappings
2. **Incomplete PR correlation**: Many commits don't reference PRs - that's OK
3. **Over-automation**: The narratives require human judgment and synthesis
4. **Scope creep**: A 5,000-word history beats a never-finished 50,000-word one
5. **Missing context**: Always read the actual PR discussions, not just titles

## Time Budget

For a mature project (5+ years, 2,000+ PRs):

- Day 1: Data fetching and automation (2-4 hours)
- Day 2: Curating significant PRs and contributors (4-6 hours)
- Day 3: Deep dives on top 20-30 PRs (6-8 hours)
- Day 4: Write first 2-3 period narratives (6-8 hours)
- Day 5: Write remaining period narratives (6-8 hours)
- Day 6: Write main overview and validate (4-6 hours)
- Day 7: Polish and final review (2-4 hours)

**Total: 30-48 hours of focused work**

## Maintenance

To update history when new developments occur:

```bash
# Re-fetch recent data
./tools/fetch-github-history --state open --verbose

# Regenerate timeline for current period
./tools/generate-history-draft --phase timelines --verbose

# Use AI to extend the current period narrative
# (use Prompt 6 with updated timeline)
```

## Questions?

This guide is based on creating a comprehensive history of the osbuild project (2019-2026, 4,000+ commits, 2,100+ PRs). Adapt the prompts and workflow to fit your project's unique characteristics.

The tools are designed to be project-agnostic - they work on any GitHub repository with standard git history.
