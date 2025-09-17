# Route Discovery Command

This command initiates the parallel discovery phase for a Japan car trip route, deploying both Route Scavenger and Route Discovery (gemini-based) agents to comprehensively identify driving information sources, stops, and route-specific attractions.

## Usage
```
/discover-route [from] [to]
```

If no route is provided, the command will automatically select the next research-needed route from `research/routes-todo.md`.

## Process Overview

### 1. Route Selection
- **With arguments**: Use the provided origin and destination names
- **Without arguments**: Parse `research/routes-todo.md` and select the first route with status "⏳ Research needed" or "🔍 Research in progress"
- Extract travel date and any route-specific context from the TODO file

### 2. Parallel Agent Deployment
Deploy **both agents simultaneously** with identical route prompts:

**Route Scavenger Agent:**
- Uses WebSearch and trusted resources for practical driving discovery
- Identifies official route sources, driving guides, and navigation resources
- Searches for scenic drives and route-specific attractions during travel period
- Cross-references existing recommendations from base itinerary
- Focuses on accessibility and practical driving information

**Route Discovery Agent (Gemini-based):**
- Uses gemini research capabilities for cultural route context
- Discovers authentic local perspectives and traditional route significance
- Researches historical background and regional cultural transitions
- Identifies cultural stops and traditional travel patterns
- Provides deeper cultural context beyond tourist driving information

### 3. Agent Instructions Template

**Common Context for Both Agents:**
```
Research comprehensive driving route information for: {ORIGIN} to {DESTINATION}

Travel Date: {TRAVEL_DATE}
Transportation: Car/driving

RESEARCH PURPOSE: Comprehensive cataloging of ALL driving options, stops, and route experiences.
This is NOT itinerary planning - discover and document everything worth knowing for later reference.

Your task is to discover and catalog:
1. Driving route information sources (navigation, highway info, scenic drive guides)
2. ALL stops, attractions, and experiences along or near the route
3. Route-specific considerations for the travel date (weather, road conditions, seasonal attractions)
4. Cultural context and significance of the route and stops along the way
5. Related route options and alternative scenic paths worth documenting

Focus on building a complete catalog of route possibilities for comprehensive research.
```

**Route Scavenger Agent Additional Instructions:**
- Use WebSearch and trusted resources from `research/trusted-resources.md`
- Prioritize official driving sources and established route guides
- Identify practical navigation information and current road conditions
- Search for scenic drives and route-specific stops during the specific travel period
- Cross-reference against existing base recommendations for the route or destinations

**Route Discovery Agent Additional Instructions:**
- Use gemini research capabilities for cultural route deep-dive
- Focus on authentic local perspectives and traditional route significance
- Research historical context and regional cultural transitions along the route
- Identify cultural practices and traditional travel experiences
- Provide traditional context beyond typical tourist driving information

### 4. Results Compilation
After both agents complete their research:

1. **Merge findings** from both agents into unified comprehensive state
2. **Eliminate source differentiation** - present integrated findings
3. **Create unified route catalog list** using todo markdown format:
   ```markdown
   ## Priority Stops for Research

   ### On-Route (No Detour)
   - [ ] {Stop name} - {Brief description and route significance}

   ### Short Detour (15-30 minutes)
   - [ ] {Stop name} - {Context and considerations for visiting}

   ### Major Detour (30+ minutes)
   - [ ] {Stop name} - {Significance and why worth the extra time}
   ```

### 5. State File Generation
Create state file: `research/state/{origin-to-destination}-route-discovery-state.md`

**Required State File Structure:**
```markdown
# {Origin} to {Destination} Route - Discovery State

**Date:** {Creation date}
**Travel Date:** {Route travel date}
**Transportation:** Car/driving
**Status:** Discovery completed

## Comprehensive Route Research Findings

### Route Information Sources Discovered
- **Official Driving Resources:** {Count and key sources}
- **Navigation & Highway Info:** {Primary navigation sources}
- **Scenic Drive Guides:** {Route-specific guides found}
- **Community Resources:** {Forum/social platforms for driving}

### Cultural and Route Context Information
- **Route Historical Significance:** {Key insights and context}
- **Regional Cultural Transitions:** {Cultural changes along route}
- **Traditional Travel Patterns:** {Historical route context}
- **Seasonal Route Considerations:** {Weather, road conditions}

## Primary Route Options

### Main Highway Route
- **Route:** {Primary highway/road} - {Estimated drive time}
- **Characteristics:** {Fastest, most direct, etc.}

### Alternative Scenic Routes
- **Route:** {Scenic route description} - {Drive time difference}
- **Highlights:** {Scenic features and characteristics}

## Priority Stops for Research

### On-Route (No Detour)
- [ ] {Stop name} - {Brief description and route significance}

### Short Detour (15-30 minutes)
- [ ] {Stop name} - {Detour time and context for visiting}

### Major Detour (30+ minutes)
- [ ] {Stop name} - {Detour time and significance justifying extra time}

## Route-Specific Considerations

### Travel Date Factors
- **Weather Conditions:** {Expected conditions for travel date}
- **Traffic Patterns:** {Peak times and congestion considerations}
- **Seasonal Road Conditions:** {Any seasonal restrictions or considerations}

### Cultural Events Along Route
- **Events/Festivals:** {Any cultural events during travel period}
- **Seasonal Attractions:** {Date-specific attractions or experiences}
- **Regional Specialties:** {Food, crafts, traditions along route}

## Research Assignments for Detailed Research

### Batch 1 - On-Route Stops
- Agent A: [On-route stops with context]
- Agent B: [On-route stops with context]

### Batch 2 - Short Detour Research
- Agent C: [Short detour stops with context]
- Agent D: [Short detour stops with context]

### Batch 3 - Major Detour Options
- Agent E: [Major detour stops with context]

## Follow-up Research Topics for Detailed Phase
- {Route-specific cultural/historical topics for deeper research}
- {Local specialties and regional experiences to investigate}
- {Seasonal attractions and route-specific considerations}
```

### 6. Update TODO Status
Update the route status in `research/routes-todo.md`:
- Change from "⏳ Research needed" to "🔍 Research in progress"
- Add reference to state file created

## Success Criteria
- Both agents complete route discovery research
- State file created with unified findings
- Priority stops organized in todo format for phase 2
- Research assignments defined for parallel detailed research
- TODO file updated with progress status

## Output
The command should conclude with:
1. Summary of route options discovered and stops prioritized
2. Path to generated state file
3. Confirmation that route is ready for Phase 2 research
4. Next recommended command: `/research-route {origin-to-destination}`