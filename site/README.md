# Japan Trip 2025

A timeline-based travel website for planning and documenting our Japan trip, built with Zola and featuring interactive Google Maps.

## Quick Start

### Prerequisites
- [Zola](https://www.getzola.org/documentation/getting-started/installation/) static site generator
- [uv](https://docs.astral.sh/uv/) for Python dependency management (optional, for content generation)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd japan-trip-2025
   ```

2. **Configure Google Maps API** (for interactive maps)
   ```bash
   cd site
   cp config.local.toml.example config.local.toml
   # Edit config.local.toml and add your Google Maps API key
   ```

3. **Generate content from research**
   ```bash
   uv run python scripts/generate_timeline.py
   ```

4. **Start development server**
   ```bash
   cd site
   zola serve --config config.local.toml
   ```

5. **Visit** http://127.0.0.1:1111

## Google Maps API Setup

The site uses Google Maps to display attraction locations on destination and route pages.

### Getting an API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/google/maps-apis)
2. Create a new project or select existing
3. Enable **Maps JavaScript API**
4. Create credentials → API Key
5. Copy the key to `site/config.local.toml`

### Securing Your API Key (Recommended)

In Google Cloud Console:
- **Application restrictions**: HTTP referrers
  - Add: `localhost:*/*` (development)
  - Add: `your-domain.com/*` (production)
- **API restrictions**: Restrict to "Maps JavaScript API" only
- **Set daily quota**: e.g., 1000 requests/day

### Free Tier
Google Maps includes 28,000 map loads per month for free.

## Development Workflow

1. Add research to `research/` folders
2. Ensure attractions include Google Maps coordinates
3. Generate content: `uv run python scripts/generate_timeline.py`
4. Preview: `cd site && zola serve --config config.local.toml`

## Documentation

See [CLAUDE.md](./CLAUDE.md) for complete documentation.
