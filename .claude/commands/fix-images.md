# Fix Images Command

**Usage:** `/fix-images [destination]`

**Arguments:**
- `destination` (optional): Specific destination slug to check (e.g., `tokyo`, `kyoto`). Omit to check all files.

**Purpose:** Validate attraction images and fix broken ones using parallel agents to find replacements from Wikipedia Commons.

## Command Workflow

### Phase 1: Quick Validation
1. Run `python scripts/find_broken_images.py [destination]` to identify broken images
   - Omit `[destination]` to check all files
   - Specify destination slug (e.g., `tokyo`) to check only that destination
2. Generate list of broken image URLs with file locations

### Phase 2: Parallel Agent Replacement
1. Deploy 3-5 parallel general-purpose agents
2. Each agent finds replacement for 1 broken image
3. Agents search Wikipedia Commons first, then other free sources
4. Return FIRST working image URL found (no perfectionism)

### Phase 3: Update Files
1. Replace broken URLs in research files
2. Regenerate site content with `python scripts/generate_timeline.py`

## Agent Prompt Template
```
QUICK TASK: Find the FIRST working Wikipedia Commons image URL for [DESCRIPTION].

Search Wikipedia Commons and return the FIRST high-quality image URL you find. Don't spend time looking for the perfect image.

Current broken URL: [BROKEN_URL]

Return ONLY the working image URL, nothing else.
```

## Implementation
- Use `scripts/find_broken_images.py` for validation
- Deploy parallel Task agents for image replacement
- Update research markdown files directly
- Regenerate site content after fixes