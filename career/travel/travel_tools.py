# travel_tools.py
from agents import function_tool

@function_tool
def get_flights(destination: str) -> str:
    return f"Flights found to {destination}: PKR 45,000 - PKR 70,000."

@function_tool
def suggest_hotels(destintion: str) -> str:
    return f"Hotels in {destintion}: pearl Continental,Marriot, Local Guest Houses."