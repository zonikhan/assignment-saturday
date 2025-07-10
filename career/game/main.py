# main.py

import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from game_tools import roll_dice, generate_event
import asyncio

load_dotenv()
client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
config = RunConfig(model=model, tracing_disabled=True)

narrator_agents = Agent(
    name="NarratorAgent",
    instructions="you narrate the  adventure, Ask the player for choices.",
    model=model
)
monster_agents =Agent(
    name="MonsterAgents",
    instructions="you handle monster encounters using roll_dice and ganerate_events.",
    model=model,
    tools=[roll_dice, generate_event]
)
item_agent = Agent(
    name="ItemAgents",
    instructions="you provide rewards or items to the player",
    model=model

)

async def main():
    print("\U0001F3AE Welcome to Fantasy Game!")
    choice = input(" Do you enter the forest or turn back? ->")

    result1 = await Runner.run(narrator_agents, choice, run_config=config)
    print("\n Story:", result1.final_output)
    
    result2 = await Runner.run(monster_agents, "Start encounter", run_config=config)
    print("\n Encounter:", result2.final_output)



    result3 = await Runner.run(item_agent, "Give reward", run_config=config)
    print("\n Reward:", result3.final_output)

if __name__ == "__main__":
    asyncio.run(main())




