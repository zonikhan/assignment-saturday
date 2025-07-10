# main.py
import asyncio
import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from travel_tools import get_flights, suggest_hotels

load_dotenv()
client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
config = RunConfig(model=model, tracing_disabled=True)

destination_agent = Agent(
    name="DestinationAgent",
    instructions="You recommend travel destinations based on user's mood.",
    model=model
)
booking_agent = Agent(
    name="BookingAgent",
    instructions="You give flight and hotel info using tools.",
    model=model,
    tools=[get_flights, suggest_hotels]
)
explore_agent = Agent(
    name="ExploreAgent",
    instructions="You suggest food & places to explore in the destination.",
    model=model
)

async def main():
    print("\U0001F30D AI Travel Designer\n")
    mood = input("✈️ What's your travel mood (relaxing/adventure/etc)? → ")

    result1 = await Runner.run(destination_agent, mood, run_config=config)
    dest = result1.final_output.strip()
    print("\n📍 Destination Suggested:", dest)

    result2 = await Runner.run(booking_agent, dest, run_config=config)
    print("\n✈️ Booking Info:", result2.final_output)

    result3 = await Runner.run(explore_agent, dest, run_config=config)
    print("\n🍽️ Explore Tips:", result3.final_output)

if __name__ == "__main__":
    asyncio.run(main())
