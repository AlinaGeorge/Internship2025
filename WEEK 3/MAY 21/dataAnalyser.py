import asyncio
import pandas as pd
import os
import matplotlib.pyplot as plt
from dotenv import load_dotenv

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console

load_dotenv()

# Tool 1: Fetch CSV and return file path
async def fetch_csv(file_path: str) -> str:
    await asyncio.sleep(1)
    # Validate the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exist.")
    return file_path

# Tool 2: Load CSV and analyze data from file path
async def analyze_data(file_path: str, output_file: str) -> str:
    await asyncio.sleep(1)
    data = pd.read_csv(file_path)
    if "Name" not in data.columns or "Age" not in data.columns:
        return "Required columns not found in the data."

    plt.figure(figsize=(10, 6))
    data.plot(kind="bar", x="Name", y="Age")
    plt.title("Data Visualization")
    plt.savefig(output_file)
    plt.close()
    return f"Visualization saved to {output_file}"

async def main():
    model_client = OpenAIChatCompletionClient(
        model="gemini-1.5-flash-8b",
        api_key=os.getenv("API_KEY")
    )

    data_fetcher = AssistantAgent(
        name="DataFetcher",
        description="Fetches CSV file paths.",
        model_client=model_client,
        system_message="You are a data fetcher. Use the fetch_csv tool to return the path of a CSV file.",
        tools=[fetch_csv],
    )

    analyzer = AssistantAgent(
        name="Analyzer",
        description="Analyzes and visualizes data from CSV file path.",
        model_client=model_client,
        system_message="You are an analyst. Use the analyze_data tool with a file path to create a plot and save it. When done, say TERMINATE.",
        tools=[analyze_data],
    )

    termination = TextMentionTermination("TERMINATE")

    group_chat = RoundRobinGroupChat(
        [data_fetcher, analyzer],
        termination_condition=termination,
        max_turns=5
    )

    await Console(group_chat.run_stream(
        task="Use the file 'data.csv' and generate a bar chart of Name vs Age. Save the visualization as 'graph.png'."
    ))

    await model_client.close()

if __name__ == "__main__":
    asyncio.run(main())
