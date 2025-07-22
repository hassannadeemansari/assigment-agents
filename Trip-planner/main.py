
# chaanginng in api key only all is correct


import os

from agents import (
    Agent,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    Runner,
    handoff
)
from agents.run import RunConfig
from dotenv import load_dotenv
# def tool(func):
#     return func

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("GEMINI_API_KEY is not set , Please ensure it is defined in you .env.file!")

external_client = AsyncOpenAI(
    api_key = openai_api_key,
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client = external_client
)

config = RunConfig(
    model = model,
    model_provider = external_client,
    tracing_disabled = True
)

Destination_agent = Agent(
                         name = "Destination_agent" , 
                         instructions = """you are a destination_agent who suggest user to find best places who helps user to find best
                         destination basically you provide good destination to user for better experience , your are only
                         for provide detination to user"""
                        )

Booking_agent = Agent(
                         name = "booking_agent" ,
                         instructions = """you are a booking agent that help user to provide all booking details like suggest hotel
                         , provide cost of rent for every hotel , Provide Schedule Your work is only as booking agent""")

Explore_Agent = Agent(
                         name = "explore_agent" ,
                         instructions = """your are a Exploring Agent an your work is to provide or suggest Arraction or foods or
                         culture of place based on its destination and its hotel or place or famous things about that places """)

trip_planner = Agent(
                         name = "Trip Planner" , 
                         instructions = """you are a Agent who work is to read user querry and see what user asking about like Destination , place etc ...  or
                         asking about booking of hotel or price for stay or place of stay etc.. or asking about exploring famous food agricultre or like things etc.... so basically
                         your works is to handoff to Destination_agent , Booking_agent , Explore_Agent  based on user querry...""" , 
                         handoffs = [Destination_agent , Booking_agent , Explore_Agent]   
                    )
 

response = input("hi! how can i help you in your trip? ")
result = Runner.run_sync(trip_planner , response , run_config = config)

print(result.final_output)



