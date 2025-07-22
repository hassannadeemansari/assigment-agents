import os

from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    AsyncOpenAI,
    RunConfig,
    handoff
)
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url = "https://generativelanguage.googleapis.com/v1beta"
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client = external_client,
    
)

config = RunConfig(
    model = model,
    model_provider = external_client,
    tracing_disabled = True
)

Career_Agent = Agent(
    name = "Career-Agent",
    instructions = "you are a career agent who suggest the best field based on user interest"
)

Skill_Agent = Agent(
    name = "Skill-Agent",
    instructions = "you are a agent whose work is to shows skills building plans on the based of suggest field or based on user interested field"
)

Job_Agent = Agent(
    name = "Job-Agent",
    instructions = " you are a job agent who shares the real world job roles on industry level based on user skill , field or based on user interested field "    
)

Career_Mentor = Agent(
    name = "Career-mentor",
    instructions = " you are career mentor agent which work is to handoff the question to its expert agent not give answere by yourself or your own only use handoff ",
    handoffs = [Career_Agent , Skill_Agent , Job_Agent]
)

Response = input("Hi! what field are you interested in? :")
result = Runner.run_sync(Career_Mentor , Response , run_config = config)

print(result.final_output)