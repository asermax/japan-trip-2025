# Detailed Location Research Command

This command conducts comprehensive detailed research on locations identified during discovery, deploying multiple Location Researcher Agents in parallel based on the research assignments from the discovery state file.

## Usage
```
/research [destination]
```

If no destination is provided, the command will automatically select the destination with the most recent discovery state file in `research/state/`.

## Prerequisites
- **Required**: Discovery must be completed
- **Required**: Discovery state file must exist: `research/state/{destination-slug}-discovery-state.md`
- **State file must contain**: Research assignments and priority locations in todo format

## Process Overview

### 1. Validation & Setup
1. **Destination Selection**:
   - **With argument**: Use provided destination and locate corresponding state file
   - **Without argument**: Find most recent `*-discovery-state.md` file in `research/state/`

2. **State File Validation**:
   - Verify discovery state file exists
   - **If missing**: Alert user and stop execution with message:
     ```
     ❌ Error: No discovery state file found for {destination}.
     Please run /discovery {destination} first to complete the discovery phase.
     ```
   - Parse state file for research assignments and context

3. **Extract Context from State File**:
   - Visit dates and accommodation details
   - Priority locations organized by tier
   - Cultural and contextual background
   - Research batch assignments
   - Date-specific events and festivals

### 2. Parallel Research Agent Deployment

Deploy **multiple Location Researcher Agents simultaneously** based on state file batch assignments:

**Agent Assignment Strategy:**
- **Batch 1**: Essential locations (Tier 1) - Deploy 2 agents in parallel
- **Batch 2**: Conditional locations (Tier 2) - Deploy 2 agents in parallel
- **Batch 3**: Backup options (Tier 3) - Deploy 1-2 agents based on list size

**Per-Agent Context Package:**
```
Research comprehensive information for your assigned locations in: {DESTINATION}

Visit Period: {VISIT_DATES} (for seasonal context and events reference)
Duration: {STAY_DURATION} (for planning context only)
Accommodation: {ACCOMMODATION_NAME} - {ACCOMMODATION_ADDRESS}

RESEARCH PURPOSE: Complete cataloging of all information about each assigned location.
This is NOT about fitting into a specific itinerary - research and document everything useful.

## Your Research Assignment
{SPECIFIC_LOCATIONS_FROM_BATCH}

## Background Context (from Discovery)
{CULTURAL_CONTEXT_FROM_STATE_FILE}
{DATE_SPECIFIC_EVENTS}
{INFORMATION_SOURCES_DISCOVERED}

## Research Focus Areas
For each assigned location, research:

### Practical Information
- Current operating hours and seasonal schedules
- Admission costs and booking requirements
- Accessibility information and transportation options
- Current operational status (open/closed/renovations)
- Best visiting times and crowd considerations

### Cultural Context & Experience
- Cultural significance and historical background
- What to expect as a visitor
- Photography guidelines and restrictions
- Cultural etiquette and proper behavior
- Local customs and traditions

### Visitor Experience
- Recent visitor reviews and experiences
- Duration recommendations and time considerations
- What makes this location special or unique
- Connections with nearby locations and attractions
- Practical tips for international visitors

## Research Instructions
- Use multiple research tools in parallel when possible
- Verify information across multiple sources
- Note seasonal considerations and optimal visiting conditions
- Cross-reference with cultural context from discovery phase
- Document all available information regardless of trip duration constraints
- Use Gemini research for cultural deep-dives when needed

## Output Format
Structure findings for each location with:
- Complete practical visiting information
- Cultural context and significance
- Visitor experience expectations and recommendations
- Connection notes with other regional attractions
- Source citations and verification dates
```

### 3. Research Coordination & Integration

**Parallel Execution Management:**
1. Launch all agent batches with their specific assignments
2. Monitor progress and coordinate cross-references between agents
3. Ensure agents can reference each other's findings for integration insights
4. Compile results maintaining priority tier context and base recommendation status

**Integration Points:**
- Cross-reference findings between related locations
- Identify timeline integration opportunities
- Note transportation connections and logical groupings
- Highlight seasonal considerations specific to visit dates

### 4. Results Compilation & Documentation

**State File Updates:**
1. Update existing state file with research completion status
2. Check off completed todo items in priority location lists:
   ```markdown
   ### Tier 1 - Essential
   - [x] {Location name} - {Research completed with key findings summary}
   - [ ] {Location name} - {Still pending research}
   ```

**Detailed Research Output:**
Create comprehensive research file: `research/destinations/{destination-slug}.md`

**Required Research File Structure:**
```markdown
# {Destination} Research

**Visit Period:** {Visit dates}
**Duration:** {Stay duration}
**Accommodation:** {Name and address}
**Research Completed:** {Date}
**Discovery State:** research/state/{destination-slug}-discovery-state.md

## Essential Locations (Tier 1)

### {Location Name}
- **Category:** {Temple/Market/District/etc}
- **Cost:** {Free/¥XXX}
- **Hours:** {Operating schedule}
- **Best Time:** {Recommendations}
- **Duration:** {Recommended visit time}
- **Accessibility:** {Transportation and access info}

**Cultural Context:** {Significance and background}

**Visitor Experience:** {What to expect, tips, etiquette}

**Timeline Integration:** {How this fits with visit schedule}

**Sources:** {Citations and verification dates}

---

## Conditional Locations (Tier 2)
{Same format as Tier 1}

## Backup Options (Tier 3)
{Same format as Tier 1}

## Date-Specific Events & Festivals
{Events occurring during visit period}

## Cultural Context & Local Insights
{Synthesized cultural information from all research}

## Logistics & Practical Information

### Transportation
{How to get around, key routes, transportation options}

### Food & Dining
{Notable restaurants, local specialties, dining customs}

### Accommodation Integration
{How location relates to lodging, nearby amenities}

### Weather & Seasonal Considerations
{Seasonal information and optimal visiting conditions}

## Regional Connections
{How locations connect within the region and complement each other}

## Research Process Notes
- **Discovery Agents Used:** Location Scavenger + Location Discovery (gemini)
- **Research Agents Deployed:** {Number} agents across {Number} batches
- **Sources Consulted:** {Primary source types}
- **Last Updated:** {Date}
- **Status:** Research completed, ready for future itinerary planning
```

### 5. TODO Status Update

Update destination status in `research/destinations-todo.md`:
- Change from "🔍 Research in progress" to "✅ Research completed"
- Add reference to completed research file

### 6. State File Completion

Update the discovery state file to reflect research completion:
- Mark all priority locations as researched: `- [x]`
- Add completion date and research file reference
- Update status to "Research completed"

## Success Criteria
- All priority locations researched by assigned agents
- Comprehensive destination research catalog created
- State file updated with completion status
- TODO file updated to reflect completed research
- Ready for future content generation and itinerary planning

## Error Handling

**Missing State File:**
```
❌ Error: Discovery state file not found for {destination}
Expected file: research/state/{destination-slug}-discovery-state.md

Please complete discovery first:
/discovery {destination}
```

**Incomplete State File:**
```
⚠️  Warning: State file exists but appears incomplete
Missing required sections: {missing_sections}

Please re-run discovery to generate complete state file.
```

## Output
The command should conclude with:
1. Summary of locations researched across all tiers
2. Path to comprehensive research file created
3. Confirmation that destination research is complete
4. Next recommended action: Research catalog ready for future itinerary planning and content generation

## Integration with Content Generation
The detailed research catalog serves as input for:
- Future itinerary planning and daily schedule creation
- `python scripts/generate_timeline.py` for timeline content creation (when ready)
- Place guide generation with comprehensive information
- Attraction page creation with cultural context and practical details