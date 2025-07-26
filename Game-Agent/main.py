import os
import random
from agents import (
    Agent,
    Runner,
    RunConfig,
    OpenAIChatCompletionsModel,
    AsyncOpenAI
)
from dotenv import load_dotenv


load_dotenv() 
gemini_api_key = os.getenv("GEMINI_API_KEY")


external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

def roll_dice():
    return random.randint(1, 20)


def generate_event(context: str = ""):
    """Generate random events based on game context."""
    events = [
        "You encounter a mysterious traveler on the road.",
        "A sudden storm forces you to take shelter.",
        "You find strange footprints leading off the path.",
        "A distant sound catches your attention.",
        "Everything seems quiet... too quiet.",
        "A rare bird flies overhead, dropping a shiny object.",
        "You stumble upon an ancient stone marker with strange inscriptions.",
        "A hidden trapdoor reveals a secret passage beneath your feet.",
        "A merchant appears, offering exotic goods from distant lands.",
        "A magical portal shimmers into existence nearby."
    ]
    return random.choice(events)

game_tools = [roll_dice, generate_event]


NarratorAgent = Agent(
    name="Narrator",
    instructions="You are the storyteller of a fantasy adventure. Describe the world, settings, and narrative based on player choices. "
                "Keep descriptions vivid but concise. Advance the story based on player actions and dice rolls. "
                "Use generate_event to introduce unexpected developments."
)

MonsterAgent = Agent(
    name="MonsterMaster",
    instructions="You manage all combat encounters. Describe monsters, their actions, and resolve combat turns. "
                "Use roll_dice to determine attack success and damage. Keep combat exciting but fair. "
                "Provide vivid descriptions of creatures and their abilities."
)

ItemAgent = Agent(
    name="ItemMaster",
    instructions="You manage the player's inventory and item interactions. Describe found items, their properties, "
                "and how they can be used. Handle rewards and equipment management. "
                "Be creative with magical items and their effects."
)

GameMaster = Agent(
    name="GameMaster",
    instructions="""You are the Game Master for a text-based fantasy adventure game. Your responsibilities include:
1. Managing the overall game flow and player progression
2. Deciding when to hand off control to specialized agents (Narrator, Monster, Item)
3. Using game tools like dice rolls and random events
4. Maintaining game state and consistency

Game Flow Rules:
- Start by setting the scene with NarratorAgent
- When combat begins, switch to MonsterAgent
- When items are involved, use ItemAgent
- Always maintain a fair and fun experience
- Use roll_dice for skill checks and combat
- Use generate_event for random encounters

Begin the game by welcoming the player and asking what kind of character they want to play. 
Describe the starting location and initial situation.
"""
)

#  runner 
def run_game():
    print("=== Fantasy Adventure Game ===")
    print("Type 'quit' to exit at any time\n")
    

    res = input("Welcome, adventurer! What kind of hero are you? (Describe your character): ")

    context = f"The player has chosen this character: {res}"
    current_agent = GameMaster
    
    while res.lower() != 'quit':
        try:
            result = Runner.run_sync(
                current_agent, 
                context, 
                run_config=config,
            )
            output = result.final_output
            
            print(f"\n{current_agent.name}: {output}\n")
            
            # Prompt next player input
            res = input("Your action: ")
            context += f"\nPlayer: {res}"
        
        except Exception as e:
            print(f"\nError: {e}\n")
            break

if __name__ == "__main__":
    run_game()
