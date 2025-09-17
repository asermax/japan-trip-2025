# Detailed Route Research Command

This command conducts comprehensive detailed research on stops and attractions identified during route discovery, deploying multiple Location Researcher Agents in parallel based on the research assignments from the route discovery state file.

## Usage
```
/research-route [from-to]
```

If no route is provided, the command will automatically select the route with the most recent discovery state file in `research/state/`.

## Prerequisites
- **Required**: Route discovery must be completed
- **Required**: Route discovery state file must exist: `research/state/{origin-to-destination}-route-discovery-state.md`
- **State file must contain**: Research assignments and priority stops in todo format

## Process Overview

### 1. Validation & Setup
1. **Route Selection**:
   - **With argument**: Use provided route and locate corresponding state file
   - **Without argument**: Find most recent `*-route-discovery-state.md` file in `research/state/`

2. **State File Validation**:
   - Verify route discovery state file exists
   - **If missing**: Alert user and stop execution with message:
     ```
     ❌ Error: No route discovery state file found for {origin-to-destination}.
     Please run /discover-route {from} {to} first to complete the discovery phase.
     ```
   - Parse state file for research assignments and context

3. **Extract Context from State File**:
   - Travel date and route context
   - Priority stops organized by detour level
   - Cultural and route background context
   - Research batch assignments
   - Route-specific considerations and seasonal factors

### 2. Parallel Research Agent Deployment

Deploy **multiple Location Researcher Agents simultaneously** based on state file batch assignments:

**Agent Assignment Strategy:**
- **Batch 1**: On-route stops (No detour) - Deploy 2 agents in parallel
- **Batch 2**: Short detour stops (15-30 min) - Deploy 2 agents in parallel
- **Batch 3**: Major detour stops (30+ min) - Deploy 1-2 agents based on list size

**Per-Agent Context Package:**
```
Research comprehensive information for your assigned stops along the route: {ORIGIN} to {DESTINATION}

Travel Date: {TRAVEL_DATE} (for seasonal context and route conditions)
Transportation: Car/driving
Route Context: {ROUTE_DESCRIPTION_FROM_STATE}

RESEARCH PURPOSE: Complete cataloging of all information about each assigned stop.
This is NOT about fitting into a specific itinerary - research and document everything useful.

## Your Research Assignment
{SPECIFIC_STOPS_FROM_BATCH}

## Background Context (from Route Discovery)
{ROUTE_CULTURAL_CONTEXT_FROM_STATE_FILE}
{SEASONAL_ROUTE_CONSIDERATIONS}
{ROUTE_INFORMATION_SOURCES_DISCOVERED}

## Research Focus Areas
For each assigned stop, research:

### Practical Route Information
- Current operating hours and seasonal schedules
- Parking availability and accessibility from route
- Admission costs and booking requirements
- Current operational status (open/closed/renovations)
- Time needed for visit and route impact
- Distance from main route and detour time

### Route-Specific Context & Experience
- Why this stop is significant for this specific route
- What to expect as a driving visitor
- Photography opportunities and scenic viewpoints
- Route-specific cultural significance
- Connection with route's overall journey narrative

### Driving Visitor Experience
- Recent visitor reviews focusing on route travelers
- Recommended visit duration for route travelers
- What makes this stop special for car travelers
- Connections with other stops along the route
- Practical tips for driving visitors (parking, access, facilities)

### Route Integration
- How this stop fits into the overall route experience
- Logical grouping with other route stops
- Seasonal considerations specific to travel date
- Alternative options if stop is unavailable

## Research Instructions
- Use multiple research tools in parallel when possible
- Verify information across multiple sources
- Note seasonal considerations and optimal visiting conditions for route
- Cross-reference with route context from discovery phase
- Document all available information regardless of detour time constraints
- Focus on car accessibility and driving visitor experience
- Use existing location researcher capabilities adapted for route context

## Output Format
Structure findings for each stop with:
- Complete practical visiting information for car travelers
- Route-specific context and significance
- Driving visitor experience expectations and recommendations
- Connection notes with other route stops and attractions
- Source citations and verification dates
```

### 3. Research Coordination & Integration

**Parallel Execution Management:**
1. Launch all agent batches with their specific route assignments
2. Monitor progress and coordinate cross-references between route agents
3. Ensure agents can reference each other's findings for route integration insights
4. Compile results maintaining detour level context and route flow

**Route Integration Points:**
- Cross-reference findings between related stops along route
- Identify logical stop groupings and route flow optimization
- Note seasonal considerations specific to travel date
- Highlight route-specific cultural or scenic connections

### 4. Results Compilation & Documentation

**State File Updates:**
1. Update existing state file with research completion status
2. Check off completed todo items in priority stop lists:
   ```markdown
   ### On-Route (No Detour)
   - [x] {Stop name} - {Research completed with key findings summary}
   - [ ] {Stop name} - {Still pending research}
   ```

**Detailed Research Output:**
Create comprehensive research file: `research/routes/{origin-to-destination}.md`

**Required Research File Structure:**
```markdown
# {Origin} to {Destination} Route Research

**Travel Date:** {Travel date}
**Transportation:** Car/driving
**Route Distance:** {Approximate distance and drive time}
**Research Completed:** {Date}
**Discovery State:** research/state/{origin-to-destination}-route-discovery-state.md

## Route Overview

**Primary Route:** {Main highway/road route}
**Alternative Scenic Routes:** {Alternative routes discovered}
**Estimated Drive Time:** {Base drive time without stops}

## On-Route Stops (No Detour)

### {Stop Name}
- **Type:** {Rest area/town/attraction/scenic viewpoint}
- **Location:** {Highway/road marker or town name}
- **Facilities:** {Parking, restrooms, food, etc.}
- **Visit Duration:** {Recommended time for stop}
- **Accessibility:** {Ease of access from route}

**Route Significance:** {Why this stop matters for this route}

**Driving Visitor Experience:** {What to expect, facilities, tips}

**Route Integration:** {How this fits with overall journey}

**Sources:** {Citations and verification dates}

---

## Short Detour Stops (15-30 minutes)

### {Stop Name}
- **Detour Time:** {Additional time from main route}
- **Type:** {Attraction/cultural site/scenic area}
- **Cost:** {Free/¥XXX}
- **Hours:** {Operating schedule}
- **Parking:** {Availability and cost}
- **Visit Duration:** {Recommended time}

**Route Context:** {Why worth the detour on this route}

**Driving Visitor Experience:** {What to expect, access, tips}

**Route Integration:** {Connection with other stops, route flow}

**Sources:** {Citations and verification dates}

---

## Major Detour Stops (30+ minutes)

### {Stop Name}
- **Detour Time:** {Additional time from main route}
- **Significance:** {Why this justifies major detour}
- **Type:** {Major attraction/cultural center/natural site}
- **Cost:** {Free/¥XXX}
- **Hours:** {Operating schedule}
- **Accessibility:** {Detailed access information}
- **Visit Duration:** {Recommended time}

**Route Justification:** {Why this major detour is worthwhile}

**Driving Visitor Experience:** {Comprehensive visitor information}

**Route Integration:** {Impact on overall journey, alternatives}

**Sources:** {Citations and verification dates}

---

## Route-Specific Considerations

### Seasonal Factors (for Travel Date)
{Weather conditions, road conditions, seasonal attractions}

### Traffic and Timing
{Best departure times, traffic patterns, peak periods}

### Fuel and Services
{Service areas, fuel stations, facilities along route}

### Cultural Route Context
{Cultural significance of the route, regional transitions, traditional travel patterns}

## Route Flow Recommendations

### Suggested Stop Combinations
{Logical groupings of stops that work well together}

### Alternative Route Strategies
{Different approaches based on interests, time constraints, weather}

### Route Integration with Destinations
{How route stops connect with origin and destination activities}

## Research Process Notes
- **Discovery Agents Used:** Route Scavenger + Route Discovery (gemini)
- **Research Agents Deployed:** {Number} agents across {Number} batches
- **Sources Consulted:** {Primary source types for route research}
- **Last Updated:** {Date}
- **Status:** Route research completed, ready for future itinerary planning
```

### 5. TODO Status Update

Update route status in `research/routes-todo.md`:
- Change from "🔍 Research in progress" to "✅ Research completed"
- Add reference to completed route research file

### 6. State File Completion

Update the route discovery state file to reflect research completion:
- Mark all priority stops as researched: `- [x]`
- Add completion date and research file reference
- Update status to "Research completed"

## Success Criteria
- All priority stops researched by assigned agents
- Comprehensive route research catalog created
- State file updated with completion status
- TODO file updated to reflect completed route research
- Ready for future content generation and itinerary planning

## Error Handling

**Missing State File:**
```
❌ Error: Route discovery state file not found for {origin-to-destination}
Expected file: research/state/{origin-to-destination}-route-discovery-state.md

Please complete route discovery first:
/discover-route {from} {to}
```

**Incomplete State File:**
```
⚠️  Warning: State file exists but appears incomplete
Missing required sections: {missing_sections}

Please re-run route discovery to generate complete state file.
```

## Output
The command should conclude with:
1. Summary of stops researched across all detour levels
2. Path to comprehensive route research file created
3. Confirmation that route research is complete
4. Next recommended action: Route catalog ready for future itinerary planning and content generation

## Integration with Content Generation
The detailed route research catalog serves as input for:
- Future itinerary planning and route scheduling
- `python scripts/generate_timeline.py` for timeline content creation (when ready)
- Journey page generation with comprehensive route information
- Attraction page creation for route-specific stops with driving context