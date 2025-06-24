from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel , function_tool # type: ignore
from agents.run import RunConfig # type: ignore
import os

from dotenv import load_dotenv


load_dotenv()



#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key= os.environ.get("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

@function_tool
def add(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b +22





agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant for lead Generaton , Respond in  just 25 letters " , )
inp_user = input("")
result = Runner.run_sync(agent, inp_user, run_config=config)

print(result.final_output)