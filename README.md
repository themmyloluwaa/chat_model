# Chat Model (Tutorial)

## Summary

A simple model of agents (users) chatting with other agents. All agents start with the same wealth called **quids**. Every step, one agent picks a partner to chat with based on a matching algorithm. This matching algorithm uses gender preference as the basis for a successful match.

### Matching algorithm

- Agent A picks another agent B that hasn't been matched in that from their neighbours. This step simulates partner suggestion to agent A and B silmultenously and results in a deduction of 5 quids from each agents wealth.
- A match is made when Agent A gender preference matches B and B's gender preference matches A. A match is also made if there's no match in gender preference but there's a 50% chance both of them decide to go ahead with the conversation (simulates a situation where a user might chose to chat with you even if you're not their preference).
- Once a match is made, each user gets 8 quids and a Chat happens.
- Once conversation ends, each user is rewarded with quids based on the length of their conversation.
- Both users are removed from the list of partners for other candidates to match with them.

### Chat Agent

This agent handles chats between two users and rewards each user based on the length of the chat they have. The reward is calculated as

- There's a reward of 1 quid per 2 seconds spent conversing. So chat reward is calculated as `(chat_duration // 2 )* chat_reward_per_two_seconds` where **chat_duration** is the total seconds spent chatting by the users and **chat_reward_per_two_seconds** is the reward amount per 2 seconds of conversation.

## How to Run

- First create a virtual environment and activate it.
- Run `pip install -r requirements.txt`
- Run `python run.py` to start the server.

If your browser doesn't open automatically, point it to [http://127.0.0.1:8521/](http://127.0.0.1:8521/). When the visualization loads, press Reset, then Run.

## Files

- `cr_model/model.py`: The chat model where agents are initialized.
- `cr_model/agents.py`: Contains the User agent and Chat agents.
- `server.py`: Creates and launches interactive visualization.
- `run.py`: Handles launching the server.
