# Prompt Engineering Process

**Name:** Valentina Aguirre

---

## Step 1

### Intention

My initial goal was to successfully create a working DnD LLM agent that could converse with a user, respond as a Dungeon Master, and exit cleanly using the `/exit` command so that the chat attempt could be logged for grading.

### Action / Change

I implemented the basic chat loop using `ollama.chat()` by following the structure of `demo_agent.py`. I made sure that:

* Messages were appended correctly for both user and assistant roles.
* The program exited gracefully when `/exit` was entered.
* The conversation was written to `attempts.txt` after exiting.

I also integrated the provided `dm_chat.json` template so the agent used the intended system prompt and model configuration.

### Result

The program ran successfully without syntax errors, the agent responded to user input, and `attempts.txt` was created as expected when exiting with `/exit`.

### Reflection / Analysis

This step confirmed that the core LLM workflow was correct: message formatting, looping, and exit handling. At this stage, the agent technically worked, but the responses were generic and instructional rather than an actual DnD adventure. This showed that correctness of code alone is not enough, that prompt design plays a huge role in agent behavior.

---

## Step 2

### Intention

After confirming basic functionality, my goal was to make the agent behave like an actual Dungeon Master by starting an adventure immediately instead of explaining what it could do.

### Action / Change

I analyzed the initial output and noticed that the model was responding with high-level explanations. Based on prompt engineering principles discussed in class, I:

* Removed an empty assistant message from the template that confused the model.
* Added a stronger system instruction explicitly telling the model to start the adventure immediately and avoid meta explanations.
* Replaced the empty kickoff user message with a clear starting instruction that defined the player’s HP and inventory.

### Result

The agent began producing narrative responses instead of explanations. It introduced a setting, described a situation, and offered choices to the player, which felt much closer to a real DnD experience.

### Reflection / Analysis

This demonstrated how sensitive LLMs are to initial context. Even small issues like an empty message can cause the model to default to assistant-style explanations. Explicit system instructions significantly improved behavior, reinforcing the importance of prompt clarity and role definition.

---

## Step 3

### Intention

Although the agent was now roleplaying as a Dungeon Master, I noticed limitations in the gameplay quality. The responses became repetitive, HP and inventory did not meaningfully change, and the story often looped between similar situations. My goal was to improve structure, consistency, and progression through stronger prompt constraints.

### Action / Change

I attempted to further refine the system prompt by introducing additional rules and constraints. These included:

* Enforcing a fixed output structure (Location, Threat, Narration, HP, Inventory, Choices).
* Adding stricter instructions to prevent random HP or inventory changes.
* Requiring exactly three choices every turn.
* Encouraging variety in outcomes so the story would not repeat the same scenes.

I also experimented with adding few-shot examples and adjusting model parameters (such as temperature) to reduce randomness and improve coherence.

### Result

While these changes improved formatting consistency, they also introduced unintended side effects. In some cases, the Dungeon Master produced blank outputs, became unresponsive, or took significantly longer to generate responses. Other refinements caused the agent to stall or behave unpredictably. Due to time constraints, I reverted to the earlier working version, which, while repetitive, remained stable and interactive.

### Reflection / Analysis

This step was an important learning experience. It showed that prompt engineering involves trade-offs: adding too many constraints can over-restrict the model and negatively affect usability. Although the later refinements did not fully succeed, the process helped me understand how sensitive LLMs are to prompt structure, stop conditions, and parameter choices. Reverting to a simpler, reliable prompt was a conscious design decision to prioritize stability over complexity, which is a realistic engineering choice.

---

## Overall Reflection

Through this lab, I learned that building an LLM agent is less about writing complex code and more about iteratively shaping model behavior through prompts (which bug me some times because the LLM agent would not follow these prompts AT ALL). Each step involved observing model output, diagnosing issues, and testing targeted changes. Not every refinement improved the system, but documenting both successes and failures helped me better understand the prompt engineering process. Overall, this lab gave me hands-on experience with how real LLM agents are developed, debugged, and stabilized. For a first attempt, the final result met the core goals of functionality and interaction, even if it wasn't what I initially envisioned.