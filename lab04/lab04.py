from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parents[1]))

from util.llm_utils import AgentTemplate

# Add code here
def route_from_dm_output(dm_text: str) -> str | None:
    dm_text = (dm_text or "").lower()
    if "enemy" in dm_text:
        return "enemy"
    if "npc" in dm_text:
        return "npc"
    return None
# But before here.

def run_console_chat(template_file, agent_name='Agent', **kwargs):
    '''
    Run a console chat with the given template file and agent name.
    Args:
        template_file: The path to the template file.
        agent_name: The name of the agent to display in the console.
        **kwargs: Additional arguments to pass to the AgentTemplate.from_file method.
    '''
    chat = AgentTemplate.from_file(template_file, **kwargs)
    response = chat.start_chat()
    while True:
        print(f'{agent_name}: {response}')
        try:
            response = chat.send(input('You: '))
            # Add code here to check which agent chat should be started
            if agent_name.lower() == "dm":
                route = route_from_dm_output(response)

                if route == "enemy":
                    run_console_chat("lab04_enemy.json", agent_name="Enemy")
                    return

                if route == "npc":
                    run_console_chat("lab04_npc.json", agent_name="NPC")
                    return
            # But before here.
        except StopIteration as e:
            break

if __name__ ==  '__main__':
    # Add code here to start DM chat
    encounters = """
    1) A friendly merchant (NPC)
    2) A mysterious village elder (NPC)
    3) A malisious goblin ambush in the forest (ENEMY)
    4) A fire dragon guarding a treasure (ENEMY)
    """

    run_console_chat(
        template_file="lab04_dm.json",
        agent_name="DM",
        encounters=encounters
    )
    # But before here.
    pass