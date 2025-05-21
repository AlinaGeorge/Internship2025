'''import asyncio

import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

import os
from dotenv import load_dotenv

load_dotenv()

def load_csv_from_file(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath)


def plot_column_histogram(df: pd.DataFrame, column: str):

    df[column].hist()
    plt.title(f"Histogram of {column}")
    plt.xlabel(column)
    plt.ylabel("Frequency")
    plt.savefig("histogram.png")
    plt.close()
    return "Histogram saved as 'histogram.png'"

async def main():
    model_client = OpenAIChatCompletionClient(
        model= "gemini-1.5-flash",
        api_key=os.getenv("API_KEY")
    )


# Define assistant agents with asyncio
    data_fetcher = AssistantAgent(
        name="data_fetcher",
        model_client=model_client,
        description="A helpful assistant that can fetch data.",
        system_message="You are a helpful assistant that can retrieve data from CSV file.",
        tools=[load_csv_from_file]
        
        )

    analyst= AssistantAgent(
        name="analyst",
        model_client=model_client,
        description="A analyst that analysis data fetched from CSV file and generates visualizations.",
        system_message="You are a helpful assistant that can analyze data and generate visualizations.",
        tools=[plot_column_histogram]
        )

    task_prompt = """
            You are part of a Data Analysis Pipeline.

            1. `data_fetcher`: Use `load_csv_from_file("data.csv")` to read the CSV file.
            2. Pass the DataFrame to `analyst`.
            3. `analyst`: Analyze the DataFrame and create a histogram of the 'Score' column using `plot_column_histogram(df, "Score")`.
            End the session by saying 'TERMINATE'.
            """

    termination = TextMentionTermination("TERMINATE")
    group_chat = RoundRobinGroupChat(
            [data_fetcher,analyst], termination_condition=termination
        )
    await Console(group_chat.run_stream(task=task_prompt))

    await model_client.close()


# Run the async function
if __name__ == "__main__":
    asyncio.run(main())'''

import asyncio
import pandas as pd
import os
import matplotlib.pyplot as plt
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from dotenv import load_dotenv

load_dotenv()

async def fetch_csv(file_path:str)->pd.DataFrame:
    await asyncio.sleep(1)
    return pd.read_csv(file_path)

async def analyze_data(data:pd.DataFrame,output_file:str):
    await asyncio.sleep(1)
    required_columns=["Name","Age"]
    
    plt.figure(figsize=(10,6))
    data.plot(kind="bar",x="Name",y="Age")
    plt.title("Data Visualization")
    plt.savefig(output_file)
    plt.close()

async def main():
    model_client=OpenAIChatCompletionClient(
        model="gemini-1.5-flash-8b",
        api_key=os.getenv("API_KEY")
    )

    data_fetcher=AssistantAgent(
        name="DataFetcher",
        description="Fetches CSV data and return as Dataframes",
        model_client=model_client,
        system_message="You are data fetching agent,Your task to fetch the data from csv and return as Dataframe"
    )

    analyst=AssistantAgent(
        name="Analyzer",
        description="Analyze the data and create visualization",
        model_client=model_client,
        system_message="You are analyst agent,Your task to analyze the data and create visualization"
    )

    termination=TextMentionTermination("TERMINATE")
    group_chat=RoundRobinGroupChat(
        [data_fetcher,analyst],
        max_turns=3
    )

    filepath="data.csv"
    output_file="visualization.png"
    data=await fetch_csv(filepath)
    print("Data fetched")

    await analyze_data(data,output_file)
    await Console(group_chat.run_stream(task=f"Analyze the data and visualize results for {filepath}"))

if __name__ == "__main__":
    asyncio.run(main())