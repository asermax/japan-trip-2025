# Fix Orphaned Attractions Command

You are tasked with fixing orphaned attractions across multiple route files by deploying parallel agents.

## Process

1. **Run Discovery Script**
   - Execute `uv run python scripts/find_orphaned_attractions.py` to find all orphaned attractions
   - Parse the JSON output to identify routes with orphaned attractions

2. **Deploy Parallel Agents**
   - For each route with orphaned attractions, deploy a specialized agent
   - Launch agents in parallel (all in a single message with multiple Task tool calls)
   - Each agent receives:
     - Route name and route file path
     - List of orphaned attractions with slugs, titles, and categorization (on_route/short_detour/major_detour)
     - Task to add proper sections and references to the route file

3. **Agent Instructions**
   Each agent should:
   - Read the route file
   - For each orphaned attraction:
     - Read the attraction file to get the full title
     - Determine the appropriate section (On-Route Stops, Short Detour Stops, Major Detour Stops)
     - Check if the section exists; if not, create it before "Route-Specific Considerations"
     - Add the attraction with this format:
       ```markdown
       ### {title}

       [Research File: research/attractions/{route-name}/{slug}.md]

       ---
       ```
   - Verify each addition doesn't create duplicates
   - Write back the updated route file

4. **Collect Results**
   - Wait for all agents to complete
   - Report summary of routes fixed and attractions added
   - Note any errors or issues encountered

## Agent Task Template

For each route, the agent task should be:

```
Fix orphaned attractions in {route_name}

Route file: {route_file_path}

Orphaned attractions to add:

On-Route Stops (no detour):
- slug: {slug}, title: {title}, file: {attraction_file}
[... more on-route ...]

Short Detour Stops (15-30 minutes):
- slug: {slug}, title: {title}, file: {attraction_file}
[... more short detour ...]

Major Detour Stops (30+ minutes):
- slug: {slug}, title: {title}, file: {attraction_file}
[... more major detour ...]

Instructions:
1. Read the route file
2. For each attraction, verify the title from the attraction file
3. Find or create the appropriate section
4. Add each attraction with format:
   ### {title}

   [Research File: research/attractions/{route-name}/{slug}.md]

   ---
5. Check for duplicates before adding
6. Write the updated route file
7. Report what was added

Do not regenerate timeline content - only update the route files.
```

## Success Criteria

- All orphaned attractions are properly referenced in their route files
- Attractions are in the correct sections based on detour level
- No duplicates are created
- All route files remain valid markdown
- Summary report shows all changes made

## Notes

- This is similar to the /fix-images workflow using parallel agents
- Each agent works independently on a single route
- The discovery script categorizes attractions by analyzing their content
- Agents should verify categorization by reading attraction files
