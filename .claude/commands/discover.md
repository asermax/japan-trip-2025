# Location Discovery Command

This command initiates the parallel discovery phase for a Japan trip destination, deploying both Location Scavenger and Location Discovery (gemini-based) agents to comprehensively identify information sources, attractions, and related locations.

## Usage
```
/discovery [destination]
```

If no destination is provided, the command will automatically select the next research-needed destination from `research/destinations-todo.md`.

## Process Overview

### 1. Destination Selection
- **With argument**: Use the provided destination name
- **Without argument**: Parse `research/destinations-todo.md` and select the first destination with status "⏳ Research needed" or "🔍 Research in progress"
- Extract accommodation details, visit dates, and duration from the TODO file

### 2. Parallel Agent Deployment
Deploy **both agents simultaneously** with identical location prompts:

**Location Scavenger Agent:**
- Uses WebSearch and trusted resources for practical discovery
- Identifies official tourism sources and travel guides
- Searches for seasonal/date-specific events during visit period
- Cross-references existing recommendations from base itinerary
- Focuses on accessibility and practical visitor information

**Location Discovery Agent (Gemini-based):**
- Uses gemini research capabilities for cultural context
- Discovers authentic local perspectives and traditional significance
- Researches historical background and regional specialties
- Identifies cultural events and traditional practices
- Provides deeper cultural context beyond tourist information

### 3. Agent Instructions Template

**Common Context for Both Agents:**
```
Research comprehensive information for: {DESTINATION}

Visit Period: {VISIT_DATES}
Duration: {STAY_DURATION}
Accommodation: {ACCOMMODATION_NAME} - {ACCOMMODATION_ADDRESS}

RESEARCH PURPOSE: Comprehensive cataloging of ALL available options, attractions, and experiences.
This is NOT itinerary planning - discover and document everything worth knowing for later reference.

Your task is to discover and catalog:
1. Information sources (official tourism, travel guides, community resources)
2. ALL locations, attractions, and experiences (regardless of visit duration constraints)
3. Date-specific events, festivals, or seasonal considerations for reference
4. Cultural context and significance of all discovered options
5. Related nearby locations and regional attractions worth documenting

Focus on building a complete catalog of possibilities for comprehensive research.
```

**Location Scavenger Agent Additional Instructions:**
- Use WebSearch and trusted resources from `research/trusted-resources.md`
- Prioritize official sources and established travel publications
- Identify practical visitor information and current operational status
- Search for events and festivals during the specific visit period
- Cross-reference against existing base recommendations

**Location Discovery Agent Additional Instructions:**
- Use gemini research capabilities for cultural deep-dive
- Focus on authentic local perspectives and traditional significance
- Research historical context and regional specialties
- Identify cultural practices and their modern adaptations
- Provide traditional context beyond typical tourist information

### 4. Results Compilation
After both agents complete their research:

1. **Merge findings** from both agents into unified comprehensive state
2. **Eliminate source differentiation** - present integrated findings
3. **Create unified catalog list** using todo markdown format organized by type:
   ```markdown
   ## Research TODO List

   ### {Category Name - e.g., Cultural & Historic Sites}
   - [ ] {Location name} - {Brief description and significance}

   ### {Category Name - e.g., Natural & Scenic Attractions}
   - [ ] {Location name} - {Context and key features}

   ### {Category Name - e.g., Traditional Experiences}
   - [ ] {Location name} - {Experience type and cultural context}
   ```

   **Category Guidelines:**
   - Organize by attraction type, not priority tiers
   - Common categories include: Cultural & Historic Sites, Natural & Scenic Attractions, Traditional Experiences, Entertainment & Museums, Dining Experiences
   - New categories can be created as needed based on discoveries
   - Within each category, order by importance/significance

### 5. State File Generation
Create state file: `research/state/{destination-slug}-discovery-state.md`

**Required State File Structure:**
```markdown
# {Destination} - Discovery State

**Date:** {Creation date}
**Visit Period:** {Visit dates}
**Accommodation:** {Accommodation name and address}
**Status:** Discovery completed - ready for detailed research

## Research TODO List

### {Category Name - e.g., Cultural & Historic Sites}
- [ ] {Location name} - {Brief description and significance}

### {Category Name - e.g., Natural & Scenic Attractions}
- [ ] {Location name} - {Context and key features}

### {Category Name - e.g., Traditional Experiences}
- [ ] {Location name} - {Experience type and cultural context}

### {Category Name - e.g., Entertainment & Museums}
- [ ] {Location name} - {Activity type and highlights}

### {Category Name - e.g., Dining Experiences}
- [ ] {Location name} - {Cuisine type and specialties}

### Cultural Research & Context
- [ ] {Cultural significance topic} - {Research scope and importance}
- [ ] {Historical background area} - {Background and cultural relevance}
- [ ] {Local customs topic} - {Tradition and modern practice context}
- [ ] {Regional specialty research} - {Cultural and historical significance}
- [ ] {Seasonal tradition topic} - {Cultural practice and visitor relevance}

### Events & Festivals (Date-Specific)
- [ ] {Event/Festival name} - {Duration, locations, cultural significance}
- [ ] {Seasonal celebration} - {Cultural context and visitor experience}

### Practical Research Topics
- [ ] {Transportation topic} - {System details and visitor navigation}
- [ ] {Cultural etiquette topic} - {Proper behavior and cultural sensitivity}
- [ ] {Seasonal consideration} - {Weather, timing, and practical preparation}
- [ ] {Regional logistics topic} - {Local systems and visitor integration}
```

### 6. Update TODO Status
Update the destination status in `research/destinations-todo.md`:
- Change from "⏳ Research needed" to "🔍 Research in progress"
- Add reference to state file created

## Success Criteria
- Both agents complete discovery research
- State file created with unified findings
- Priority locations organized in todo format for phase 2
- Research assignments defined for parallel detailed research
- TODO file updated with progress status

## Output
The command should conclude with:
1. Summary of locations discovered and prioritized
2. Path to generated state file
3. Confirmation that destination is ready for Phase 2 research
4. Next recommended command: `/research {destination}`