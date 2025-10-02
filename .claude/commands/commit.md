# Commit Changes Command

**Usage:** `/commit [message]`

**Arguments:**
- `message` (optional): Custom commit message. If omitted, command will analyze changes and generate appropriate messages.

**Purpose:** Intelligently commit changes by scope, handling config files appropriately and creating separate commits for different types of changes.

## Command Workflow

### Phase 1: Analyze Changes

1. **Check git status** to identify all modified, added, and deleted files
2. **Categorize changes** by type:
   - **Research files**: `research/destinations/`, `research/attractions/`, `research/routes/`
   - **Code changes**: `scripts/`, Python files, configuration templates
   - **Documentation**: `CLAUDE.md`, `README.md`, command files in `.claude/`
   - **Site content**: `site/content/`, `site/templates/`, `site/static/`
   - **Configuration**: `site/config.toml`, `.gitignore`, other config files
   - **Task files**: `tasks/` directory (typically gitignored)

3. **Handle config.toml specially**:
   - If `site/config.toml` has changes, use `git diff site/config.toml` to check modifications
   - Identify if changes are API key related (lines containing `google_maps_api_key` or similar)
   - If ONLY API key changes: Skip committing config.toml
   - If OTHER changes exist: Stage only non-API-key changes using:
     ```bash
     # Temporarily stash API key changes if needed, or use selective staging
     # This may require manual intervention - inform user
     ```
   - Inform user if config.toml contains mixed changes that need manual handling

### Phase 2: Group Changes by Scope

Create separate commit groups based on logical scope:

**Research Commits** (destinations, attractions, routes):
- Group by destination if possible (e.g., "All Fujikawaguchiko research")
- Or by research phase (e.g., "Discovery state files for Takayama routes")
- Conventional commit type: `feat` for new research, `docs` for updates

**Code Commits** (scripts, tools):
- Group related code changes together
- Separate script changes from structural changes
- Conventional commit type: `feat`, `fix`, `refactor`, `perf`

**Documentation Commits**:
- CLAUDE.md updates
- Command file additions/changes
- README updates
- Conventional commit type: `docs`

**Site Content Commits**:
- Generated content updates (usually happens after research)
- Template or styling changes
- Conventional commit type: `feat` for new pages, `style` for CSS/design

**Configuration Commits**:
- .gitignore updates
- Non-API-key config changes
- Conventional commit type: `chore`

### Phase 3: Generate Commit Messages

For each commit group, generate a conventional commit message:

**Format:**
```
<type>(<scope>): <subject>

<body>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Type values:**
- `feat`: New feature or research content
- `docs`: Documentation updates
- `fix`: Bug fixes or corrections
- `refactor`: Code restructuring
- `style`: Formatting, CSS, visual changes
- `chore`: Configuration, tooling, gitignore
- `perf`: Performance improvements

**Subject guidelines:**
- Use imperative mood ("add" not "added")
- No period at end
- Max 72 characters
- Be specific but concise

**Body guidelines:**
- Explain what and why, not how
- List major changes as bullet points
- Include context for research (e.g., "Research completed for Nov 1-2 visit")

### Phase 4: Execute Commits

1. **Present commit plan** to user:
   ```
   Proposed commits:

   1. feat(research): add Fujikawaguchiko destination and attractions
      - Files: research/destinations/fujikawaguchiko.md, research/attractions/fujikawaguchiko/*.md

   2. chore(config): add tokyo-todo.md to gitignore
      - Files: .gitignore

   3. docs(commands): add commit command documentation
      - Files: .claude/commands/commit.md
   ```

2. **Ask for confirmation** unless `--yes` flag provided

3. **Execute commits** in order:
   ```bash
   git add <files-for-commit-1>
   git commit -m "message-1"

   git add <files-for-commit-2>
   git commit -m "message-2"
   ```

4. **Report results**:
   - Show commit SHAs
   - Confirm all changes committed
   - Warn about any unstaged changes remaining

## Special Cases

### Config.toml with Mixed Changes

If `site/config.toml` contains both API key changes and other changes:

1. **Alert user**:
   ```
   ⚠️  site/config.toml contains both API key changes and other modifications.

   API key changes (will be excluded):
   - Line 42: google_maps_api_key = "..."

   Other changes (will be committed):
   - Line 15: site_title = "Japan Trip 2025"
   ```

2. **Options**:
   - Use `git add -p site/config.toml` for interactive staging (recommended)
   - Manually edit and stage specific lines
   - Skip config.toml entirely and warn user

### No Changes to Commit

If `git status` shows no changes:
```
✓ Working directory clean - nothing to commit
```

### Only Gitignored Files Changed

If only files in `tasks/` or other gitignored directories changed:
```
ℹ️  Only gitignored files have changes:
- tasks/pending/0302-research-itoshima-batch-1.md
- tasks/completed/0301-create-batches-itoshima.md

These files are intentionally excluded from git. No commits needed.
```

## Command Options

**Flags:**
- `--yes` or `-y`: Skip confirmation, execute all commits automatically
- `--dry-run` or `-n`: Show commit plan without executing
- `--message <msg>` or `-m <msg>`: Use custom message for single commit (commits all changes together)

## Examples

**Example 1: Research completion**
```
/commit
```
Result:
```
Analyzing changes...

Proposed commits:
1. feat(research): add Kumamoto destination research
   - Created research/destinations/kumamoto.md
   - Added 12 attraction files in research/attractions/kumamoto/

2. chore(config): update gitignore for tokyo-todo
   - Added research/tokyo-todo.md to gitignore

Proceed? (yes/no)
```

**Example 2: Custom message for quick commit**
```
/commit -m "fix: correct image URLs in Takayama attractions"
```
Result: Single commit with custom message for all staged/unstaged changes

**Example 3: Dry run**
```
/commit --dry-run
```
Result: Shows commit plan without executing

## Implementation Notes

1. **Use bash tools** for git operations
2. **Parse git diff** to detect API key changes in config files
3. **Group intelligently** - prefer fewer meaningful commits over many tiny commits
4. **Validate** commit message format follows conventional commits
5. **Handle errors** gracefully (merge conflicts, staged changes, etc.)
6. **Preserve user intent** - if user provides custom message, use it as-is

## Error Handling

**Merge conflicts:**
```
❌ Error: Merge conflicts detected
Please resolve conflicts before committing:
- research/destinations/osaka.md
```

**Staged changes exist:**
```
ℹ️  Staged changes detected. Include in commits? (yes/no)
```

**Invalid git state:**
```
❌ Error: Not a git repository or git not available
```

## Success Output

```
✓ Changes committed successfully

Commits created:
- a1b2c3d feat(research): add Kumamoto destination research
- e4f5g6h chore(config): update gitignore for tokyo-todo

All changes committed. Working directory clean.
```
