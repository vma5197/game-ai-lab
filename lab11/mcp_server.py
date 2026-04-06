"""
DnD MCP Server - Lab 11
===================================
Complete implementation of the MCP server with three DnD-related tools.
"""

import random
from fastmcp import FastMCP


# Sample character data - use this for get_character_stat
CHARACTERS = {
    "fighter": {
        "strength": 16,
        "dexterity": 14,
        "constitution": 15,
        "intelligence": 10,
        "wisdom": 12,
        "charisma": 8
    },
    "wizard": {
        "strength": 8,
        "dexterity": 14,
        "constitution": 12,
        "intelligence": 18,
        "wisdom": 15,
        "charisma": 10
    },
    "rogue": {
        "strength": 10,
        "dexterity": 18,
        "constitution": 12,
        "intelligence": 14,
        "wisdom": 10,
        "charisma": 14
    }
}

# Create the MCP server instance
mcp = FastMCP("dnd-tools-server")

@mcp.tool()
def roll_dice(n_dice: int, sides: int, modifier: int = 0) -> str:
    """
    Roll n_dice dice with the given number of sides, plus a modifier.
    Example: roll_dice(2, 6, 3) -> "Rolled 2d6+3: [4, 2] + 3 = 9"
    """
    rolls = [random.randint(1, sides) for _ in range(n_dice)]
    total = sum(rolls) + modifier
 
    modifier_str = f"+{modifier}" if modifier > 0 else (f"{modifier}" if modifier < 0 else "")
    dice_str = f"{n_dice}d{sides}{modifier_str}"
 
    if modifier != 0:
        return f"Rolled {dice_str}: {rolls} + {modifier} = {total}"
    else:
        return f"Rolled {dice_str}: {rolls} = {total}"


@mcp.tool()
def get_character_stat(character: str, stat: str) -> str:
    """
    Look up a character's stat from the CHARACTERS dict.
    Example: get_character_stat("fighter", "strength") -> "Fighter's strength is 16"
    """
    character = character.lower()
    stat = stat.lower()
 
    if character not in CHARACTERS:
        available = ", ".join(CHARACTERS.keys())
        return f"Unknown character '{character}'. Available characters: {available}"
 
    if stat not in CHARACTERS[character]:
        available = ", ".join(CHARACTERS[character].keys())
        return f"Unknown stat '{stat}'. Available stats: {available}"
 
    value = CHARACTERS[character][stat]
    return f"{character.capitalize()}'s {stat} is {value}"


@mcp.tool()
def calculate_damage(base_damage: int, armor_class: int, attack_roll: int) -> str:
    """
    Calculate damage dealt based on attack roll vs armor class.

    TODO:
    - If attack_roll >= armor_class, the attack hits (return base_damage info)
    - Otherwise, the attack misses (0 damage)
    - Return a descriptive message
    """
    if attack_roll >= armor_class:
        return (
            f"Hit! Attack roll {attack_roll} meets AC {armor_class}. "
            f"Damage dealt: {base_damage}"
        )
    else:
        return (
            f"Miss! Attack roll {attack_roll} does not meet AC {armor_class}. "
            f"Damage dealt: 0"
        )


if __name__ == "__main__":
    mcp.run(transport="stdio")
