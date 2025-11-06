# Pokemon MCP Server

An MCP (Model Context Protocol) server built with FastMCP that provides Pokemon information including height, weight, and types.

## Features

- Get Pokemon information by name or ID
- Get random Pokemon by type
- Compare two Pokemon side-by-side (Prompt)
- No API keys required (uses free PokeAPI)
- Provides height, weight, types, and base stats for any Pokemon

## Installation

### Option 1: Local Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

### Option 2: Docker

Build and run using Docker:

```bash
# Build the Docker image
docker build -t pokemon-mcp-server .

# Run the container
docker run -it pokemon-mcp-server
```

## Usage

### Local

Run the MCP server:

```bash
python pokemon_server.py
```

### Docker

The Docker container runs the server automatically when started. The server communicates via stdin/stdout as per MCP protocol.

## API

### `get_pokemon(pokemon_name: str)`

Get Pokemon information for a specified Pokemon by name or ID.

**Parameters:**
- `pokemon_name` (str): The name or ID of the Pokemon to look up (case-insensitive)

**Returns:**
- Formatted string with Pokemon information including:
  - Pokemon ID
  - Height (in meters and centimeters)
  - Weight (in kilograms)
  - Types

**Example:**
```
get_pokemon("pikachu")
get_pokemon("charizard")
get_pokemon("25")  # Can also use ID
```

### `get_random_pokemons_by_type(type_name: str, n: int = 5)`

Get n random Pokemon of a specified type.

**Parameters:**
- `type_name` (str): The type name (e.g., "fire", "water", "grass", "electric", etc.)
- `n` (int): Number of random Pokemon to return (default: 5)

**Returns:**
- JSON string containing a list of Pokemon names of the specified type

**Example:**
```
get_random_pokemons_by_type("fire", 10)
get_random_pokemons_by_type("water")
```

## Prompts

### `compare_pokemon(pokemon1_name: str, pokemon2_name: str)`

Compare two Pokemon based on their stats, types, and characteristics.

**Parameters:**
- `pokemon1_name` (str): The name or ID of the first Pokemon
- `pokemon2_name` (str): The name or ID of the second Pokemon

**Returns:**
- Formatted comparison string including:
  - Basic information (ID, height, weight, types) for both Pokemon
  - Base stats comparison (HP, Attack, Defense, Special Attack, Special Defense, Speed)
  - Total base stats comparison
  - Summary analysis

**Example:**
```
compare_pokemon("pikachu", "charizard")
compare_pokemon("25", "6")  # Can also use IDs
```

## How It Works

1. The server queries the PokeAPI endpoint: `https://pokeapi.co/api/v2/pokemon/{name}/`
2. Extracts height, weight, and types from the response
3. Converts height from decimeters to meters/centimeters and weight from hectograms to kilograms
4. Formats and returns the Pokemon information to the client

## Dependencies

- `fastmcp`: FastMCP framework for building MCP servers
- `requests`: HTTP library for making API requests

## API Reference

The server uses the [PokeAPI](https://pokeapi.co/) which is free and doesn't require authentication.

