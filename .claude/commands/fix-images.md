# Fix Images Command

**Usage:** `/fix-images [targets]`

**Arguments:**
- `targets` (optional): Natural language description of what to check. Can be:
  - Single destination: `osaka`, `takayama`
  - Single route pair: `kinosaki-to-itoshima`, `tokyo-to-fujikawaguchiko`
  - Multiple items: `osaka and beppu`, `all completed routes`, `all destinations from tokyo to osaka`
  - Natural language: `all routes between kinosaki and beppu`, `finished routes in routes-todo`
  - Omit to check ALL files (destinations, attractions, and routes)

**Purpose:** Validate attraction images and fix broken ones using parallel agents to find replacements from Wikipedia Commons.

## Command Workflow

### Phase 1: Parse Targets and Deploy Validation Agents

**Interpret user request and identify targets:**
1. Parse natural language to identify specific destinations, route pairs, or ranges
2. Check routes-todo.md for completion status if user requests "completed" or "finished" routes
3. Create list of distinct targets to validate

**Deploy parallel validation agents:**
1. Group targets logically (e.g., each route pair or destination gets one agent)
2. Deploy parallel general-purpose agents (one per target or target group)
3. Each agent runs `uv run python scripts/find_broken_images.py [target-slug]` for its assigned target
4. Collect broken image reports from all agents

**Example target groupings:**
- "all completed routes" → One agent per completed route pair from routes-todo.md
- "osaka and beppu" → Two agents (one for osaka, one for beppu)
- "routes from kinosaki to osaka" → One agent per route in that segment

### Phase 2: Parallel Agent Replacement
1. Collect all broken images from Phase 1 validation reports
2. Deploy parallel general-purpose agents (one per broken image)
3. Each agent finds replacement for 1 broken image
4. Agents search Wikipedia Commons first, then other free sources
5. Return FIRST working image URL found (no perfectionism)

### Phase 3: Update Files
1. Replace broken URLs in research files
2. Regenerate site content with `uv run python scripts/generate_timeline.py`

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