# Detailed Route Research Command

This command conducts comprehensive detailed research on stops and attractions identified during route discovery, deploying multiple Location Researcher Agents in parallel based on the research assignments from the route discovery state file.

## Usage
```
/research-route [route-state-file]
```

Examples:
- `/research-route tokyo-to-kyoto-main-route` - Research the main route
- `/research-route tokyo-to-kyoto-coastal-route` - Research the coastal alternative

If no route is provided, the command will list all available route state files and prompt for selection.

## Prerequisites
- **Required**: Route discovery must be completed
- **Required**: Individual route state file must exist: `research/state/{route-state-filename}.md`
- **State file must contain**: TODO list with priority stops organized by detour level

## Process Overview

### 1. Validation & Setup
1. **Route Selection**:
   - **With argument**: Use provided route state filename and locate corresponding state file
   - **Without argument**: List all available `*-route-state.md` files in `research/state/` and prompt for selection

2. **State File Validation**:
   - Verify individual route state file exists
   - **If missing**: Alert user and stop execution with message:
     ```
     ❌ Error: No route state file found: {route-state-filename}.md
     Available route state files: {list of available files}
     Please run /discover-route {from} {to} first to complete the discovery phase.
     ```
   - Parse state file for TODO list and route context

3. **Extract Context from State File**:
   - Travel date and route context
   - TODO list organized by detour level
   - Route options and cultural research topics
   - Route-specific considerations and seasonal factors

### 2. Simplified Batch Processing with File Updates

Process research using predefined 5-agent batches with **immediate file creation/updates after each batch**:

**Batch Processing Strategy:**
- **Automatic Batch Creation**: Research command automatically divides TODO list items across 5-agent batches
- **Detour-Based Selection**: Pick items from categories in state file order (On-Route → Short Detour → Major Detour)
- **Batch Size**: Each batch contains up to 5 stops assigned to 5 agents running in parallel
- **Sequential Batches**: Complete one batch before starting the next

**File Update Points:**
- After each batch completion, immediately create/update route research files
- Update state file with batch completion status and findings
- Maintain continuous availability of research progress

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
{CULTURAL_RESEARCH_TOPICS}
{ROUTE_SPECIFIC_EVENTS_AND_CONSIDERATIONS}
{PRACTICAL_ROUTE_CONSIDERATIONS}

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
- **PHOTO REQUIREMENTS**: Include at least one representative photo for each route overview and attraction file using markdown format `![Alt text](image_url)`
- **LOCATION PINS**: Add Google Maps location link at the end of each file: `**Location:** [View on Google Maps](google_maps_url)`
- **PHOTO SOURCING**: Search for official tourism photos, Wikipedia commons, or other freely available images that represent the route/stop
- Note seasonal considerations and optimal visiting conditions for route
- Cross-reference with route context from discovery phase
- Document all available information regardless of detour time constraints
- Focus on car accessibility and driving visitor experience
- Use existing location researcher capabilities adapted for route context

## Output Format
Structure findings for each route and stop with:
- **Representative photos** integrated into content for route overview and individual stops
- Complete practical visiting information for car travelers
- Route-specific context and significance
- Driving visitor experience expectations and recommendations
- Connection notes with other route stops and attractions
- Source citations and verification dates
- **Google Maps location links** for route overview and each stop
```

### 3. Automated Batch Execution & File Management

**Batch Creation Logic:**
1. **Parse TODO List**: Extract all `- [ ]` items from state file by detour category
2. **Detour Order**: Process categories in state file order (On-Route → Short Detour → Major Detour)
3. **Sequential Selection**: Pick items from first category, then second category, etc., maintaining state file order within each category
4. **Agent Assignment**: Assign up to 5 stops per batch to 5 agents running in parallel
5. **Batch Sequence**: Complete each batch fully before starting the next

**Per-Batch Execution:**
1. **Deploy Agents**: Launch 5 Location Researcher Agents with current batch assignments
2. **Process Results**: Compile findings from completed agents
3. **Update Files**:
   - Create/update route research file: `research/routes/{route-name}/{origin-to-destination}-{route-name}.md`
   - Create/update route attractions folder: `research/attractions/{route-name}/`
   - Create attraction files for route-specific stops: `research/attractions/{route-name}/{stop-slug}.md`
   - Update state file with batch completion status
4. **Update State**: Mark batch stops as completed `[x]` in state file
5. **Checkpoint**: Confirm files created/updated and available for use

**Route Integration Points (Applied Per Batch):**
- Cross-reference findings between related stops discovered in current and previous batches
- Identify logical stop groupings and route flow optimization
- Note seasonal considerations specific to travel date
- Highlight route-specific cultural or scenic connections

### 4. Incremental File Management & Updates

**Per-Batch State File Updates:**
After each batch completion, update the state file to reflect progress:
```markdown
### On-Route (No Detour)
- [x] {Stop name} - Research completed, route file updated
- [x] {Stop name} - Research completed, route file updated
- [ ] {Stop name} - Pending next batch research
```

**Incremental File Creation:**
Files are created and updated throughout the process:

**After Each Batch:**
1. **Update route research file:** `research/routes/{route-name}/{origin-to-destination}-{route-name}.md` - Add new stops researched
2. **Create/update route attractions:** Individual attraction files in `research/attractions/{route-name}/`
3. **Cross-reference updates:** Add connections discovered between current and previous batch stops

**Detailed Research Output:**
Create comprehensive research files:
- **Route Overview:** `research/routes/{route-name}/{origin-to-destination}-{route-name}.md`
- **Route Attractions:** `research/attractions/{route-name}/{stop-slug}.md` (individual files per stop)

**Required Route Overview File Structure** (`research/routes/{route-name}/{origin-to-destination}-{route-name}.md`):
```markdown
# {Origin} to {Destination} - {Route Name} Route Research

![Route overview image](image_url)
*Caption: {Brief description of the route image}*

**Travel Date:** {Travel date}
**Transportation:** Car/driving
**Route Type:** {Main/Scenic/Coastal/Mountain/etc.}
**Route Distance:** {Approximate distance and drive time}
**Research Completed:** {Date}
**Discovery State:** research/state/{origin-to-destination}-{route-name}-route-state.md

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

**Location:** [View route on Google Maps](google_maps_route_url)
```

**Required Route Stop/Attraction File Structure** (`research/attractions/{route-name}/{stop-slug}.md`):
```markdown
# {Stop Name} - {Route Name} Route Research

![Stop image](image_url)
*Caption: {Brief description of the stop image}*

**Route:** {Origin} to {Destination} - {Route Name}
**Detour Level:** {On-Route/Short Detour/Major Detour}
**Location:** {Specific location details}
**Type:** {Rest area/town/attraction/scenic viewpoint}
**Cost:** {Entry fees or cost range}
**Visit Duration:** {Recommended time for stop}
**Research Completed:** {Date}

## Basic Information
{DETAILED description, significance, and comprehensive overview from route perspective}
*Source: [Source Name](URL) - Accessed Date*

## Route Context & Accessibility
{DETAILED route-specific context, parking, accessibility from route}
*Source: [Route Source](URL) - Accessed Date*

## Driving Visitor Experience
{COMPLETE visitor experience for car travelers, facilities, what to expect}
*Source: [Experience Source](URL) - Accessed Date*

## Route Integration
{How this stop fits into overall route, connections with other stops, timing considerations}
*Source: [Integration Source](URL) - Accessed Date*

## Practical Driving Tips
{COMPREHENSIVE strategy for car travelers, parking, optimal timing, route impact}
*Source: [Tips Source](URL) - Accessed Date*

**Location:** [View on Google Maps](google_maps_url)
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