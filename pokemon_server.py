"""
MCP Server for checking Pokemon information by name.
Uses PokeAPI which doesn't require authentication.
"""

import json
import random

import requests
from fastmcp import FastMCP

mcp = FastMCP("Pokemon Server")


@mcp.tool()
async def get_pokemon(pokemon_name: str) -> str:
    """
    Get Pokemon information including height, weight, and types for a given Pokemon name.

    Args:
        pokemon_name: The name or ID of the Pokemon to look up

    Returns:
        A formatted string with Pokemon information including height, weight, and types.
    """

    try:
        # Fetch Pokemon data from PokeAPI
        pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}/"
        pokemon_response = requests.get(pokemon_url)
        pokemon_response.raise_for_status()
        pokemon_data = pokemon_response.json()

        # Extract Pokemon information
        pokemon_id = pokemon_data.get("id", "N/A")
        name = pokemon_data.get("name", pokemon_name).capitalize()
        height = pokemon_data.get("height", "N/A")  # Height in decimeters
        weight = pokemon_data.get("weight", "N/A")   # Weight in hectograms

        # Extract types
        types = []
        if "types" in pokemon_data:
            for type_info in pokemon_data["types"]:
                type_name = (
                    type_info.get("type", {}).get("name", "").capitalize()
                )
                types.append(type_name)

        # Convert height from decimeters to meters
        height_m = "N/A"
        if isinstance(height, (int, float)):
            height_m = f"{height / 10:.1f}"

        # Convert weight from hectograms to kilograms
        weight_kg = "N/A"
        if isinstance(weight, (int, float)):
            weight_kg = f"{weight / 10:.1f}"

        # Format types string
        types_str = ", ".join(types) if types else "Unknown"

        result = json.dumps(
            {
                "id": pokemon_id,
                "name": name,
                "height": height_m,
                "weight": weight_kg,
                "types": types_str,
            }
        )

        return result

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return f"Error: Pokemon '{pokemon_name}' not found. Please check the spelling and try again."
        return f"Error fetching Pokemon data: HTTP {e.response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error fetching Pokemon data: {str(e)}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


@mcp.tool()
async def get_random_pokemons_by_type(type_name: str, n: int = 5) -> str:
    """
    Get n random Pokemons of a specified type.

    Args:
        type_name: The type name (e.g., "fire", "water", "grass", "electric", etc.)
        n: Number of random Pokemons to return (default: 5)

    Returns:
        A JSON string containing a list of Pokemon names of the specified type.
    """

    try:
        # Fetch type data from PokeAPI
        type_url = f"https://pokeapi.co/api/v2/type/{type_name.lower()}/"
        type_response = requests.get(type_url)
        type_response.raise_for_status()
        type_data = type_response.json()

        # Extract Pokemon list from the response
        pokemon_list = []
        if "pokemon" in type_data:
            for pokemon_entry in type_data["pokemon"]:
                pokemon_name = pokemon_entry.get("pokemon", {}).get("name", "")
                if pokemon_name:
                    pokemon_list.append(pokemon_name)

        if not pokemon_list:
            return json.dumps({
                "error": f"No Pokemons found for type '{type_name}'",
                "pokemons": []
            })

        # Ensure n doesn't exceed the available Pokemons
        n = min(n, len(pokemon_list))

        # Select n random Pokemons
        random_pokemons = random.sample(pokemon_list, n)

        result = json.dumps({
            "type": type_name.capitalize(),
            "total_available": len(pokemon_list),
            "requested": n,
            "pokemons": random_pokemons
        })

        return result

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return json.dumps({
                "error": f"Type '{type_name}' not found. Please check the spelling and try again.",
                "pokemons": []
            })
        return json.dumps({
            "error": f"Error fetching type data: HTTP {e.response.status_code}",
            "pokemons": []
        })
    except requests.exceptions.RequestException as e:
        return json.dumps({
            "error": f"Error fetching type data: {str(e)}",
            "pokemons": []
        })
    except Exception as e:
        return json.dumps({
            "error": f"An error occurred: {str(e)}",
            "pokemons": []
        })


@mcp.prompt()
async def compare_pokemon(pokemon1_name: str, pokemon2_name: str) -> str:
    return f"""
    Use the get_pokemon tool to get the stats of pokemons {pokemon1_name} and {pokemon2_name}.
    Compare their types and stats.

    Mention which would have an advantage in a fight based on their types.
    """


if __name__ == "__main__":
    mcp.run()
