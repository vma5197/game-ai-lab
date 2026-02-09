from pathlib import Path
import sys
import json

sys.path.append(str(Path(__file__).parents[1]))

from ollama import chat
from util.llm_utils import pretty_stringify_chat, ollama_seed as seed

# Add you code below
sign_your_name = 'Valentina Aguirre'

template_path = Path(__file__).parents[1] / 'util' / 'templates' / 'dm_chat.json'
with open(template_path, 'r', encoding='utf-8') as f:
  template = json.load(f)

model = template.get('model', 'gemma3:270m')
options = template.get('options', {})
messages = template.get('messages', [])

# Remove stop tokens from the template options (can truncate output to blank)
if 'stop' in options:
  options.pop('stop')

# Force a small fast model for this lab (prevents slow "thinking" models)
model = 'gemma3:270m'

# Remove empty assistant message if the template ends with one
if len(messages) > 0 and messages[-1].get('role') == 'assistant' and messages[-1].get('content', '').strip() == '':
  messages.pop()

# Strong DM rules to enforce consistent format + state tracking
messages.append({
  'role': 'system',
  'content': (
    "You are a Dungeons & Dragons Dungeon Master running a turn-based text adventure.\n"
    "Start the adventure immediately. Do NOT explain what you can do.\n"
    "CRITICAL OUTPUT RULES:\n"
    "1) Output ONLY the following format. NO markdown, NO bold, NO extra paragraphs.\n"
    "2) Location/Threat/Narration are each ONE line.\n"
    "3) HP only changes if the narration clearly describes damage/healing.\n"
    "4) Inventory only changes if narration clearly describes gaining/losing/using items.\n"
    "5) Always provide EXACTLY 3 choices labeled A) B) C) (one line each).\n"
    "6) After the user answers, continue the story and provide NEW A/B/C choices.\n"
    "7) Fantasy setting only (no real-world places).\n"
    "\n"
    "FORMAT:\n"
    "Location: <...>\n"
    "Threat: <...>\n"
    "Narration: <...>\n"
    "HP: <number>\n"
    "Inventory: <items or Empty>\n"
    "Choices:\n"
    "A) <...>\n"
    "B) <...>\n"
    "C) <...>"
  )
})

# Few-shot examples (teach the model how to act like our DM)
messages.extend([
  {'role': 'user', 'content': 'Look around'},
  {'role': 'assistant', 'content':
    'Location: Mossy Forest Path\n'
    'Threat: Distant buzzing closes in from the trees.\n'
    'Narration: The air smells wet and rotten as the sound grows louder.\n'
    'HP: 20\n'
    'Inventory: Empty\n'
    'Choices:\n'
    'A) Investigate the buzzing carefully.\n'
    'B) Back away and search for water.\n'
    'C) Climb a tree to scout ahead.'
  },

  {'role': 'user', 'content': 'B'},
  {'role': 'assistant', 'content':
    'Location: Shallow Creek Bed\n'
    'Threat: The buzzing swarm drifts closer, blocking the path back.\n'
    'Narration: You find a trickle of water and a broken bottle half-buried in mud.\n'
    'HP: 20\n'
    'Inventory: Empty\n'
    'Choices:\n'
    'A) Fill the bottle with water.\n'
    'B) Cover yourself in mud to mask your scent.\n'
    'C) Sprint past the swarm toward the creek bend.'
  },

  {'role': 'user', 'content': 'A'},
  {'role': 'assistant', 'content':
    'Location: Shallow Creek Bed\n'
    'Threat: The swarm surges closer, drawn by movement.\n'
    'Narration: You grab the bottle and fill it quickly—water splashes as the buzzing intensifies.\n'
    'HP: 20\n'
    'Inventory: Water Bottle\n'
    'Choices:\n'
    'A) Drink now to steady yourself.\n'
    'B) Throw water to distract the swarm.\n'
    'C) Retreat into the reeds and hide.'
  },
])

options |= {'seed': seed(sign_your_name)}

options |= {
  'temperature': 0.2,
  'top_p': 0.9,
  'num_predict': 220,
  'repeat_penalty': 1.1,
}

messages.append({
  'role': 'user',
  'content': (
    "Begin now. Player: Level 1. HP: 20. Inventory: Empty. "
    "Do NOT give free items. Present 3 choices."
  )
})

while True:
  response = chat(model=model, messages=messages, stream=False, options=options)
  # Add your code below
  dm_text = response.message.content

  # If the model output is blank, retry with slightly higher token budget
  if dm_text is None or dm_text.strip() == "":
    options['num_predict'] = max(options.get('num_predict', 220), 300)
    response = chat(model=model, messages=messages, stream=False, options=options)
    dm_text = response.message.content

  print(f"DM: {dm_text}\n")
  messages.append({'role': 'assistant', 'content': dm_text})

  user_text = input("You: ").strip()
  messages.append({'role': 'user', 'content': user_text})

  # But before here.
  if messages[-1]['content'] == '/exit':
    break

# Save chat
Path('lab03').mkdir(parents=True, exist_ok=True)
with open(Path('lab03/attempts.txt'), 'a') as f:
  file_string = ""
  file_string += "-------------------------NEW ATTEMPT-------------------------\n\n\n"
  file_string += f"Model: {model}\n"
  file_string += f"Options: {options}\n\n"
  file_string += pretty_stringify_chat(messages)
  file_string += "\n\n\n------------------------END OF ATTEMPT------------------------\n\n\n"
  f.write(file_string)
