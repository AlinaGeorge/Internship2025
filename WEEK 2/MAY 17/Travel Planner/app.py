import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

import os
from dotenv import load_dotenv

load_dotenv()


async def main():
    model_client = OpenAIChatCompletionClient(
        model= "gemini-1.5-flash",
        api_key=os.getenv("API_KEY")
    )


# Define assistant agents with asyncio
    planner_agent = AssistantAgent(
        name="planner_agent",
        model_client=model_client,
        description="A helpful assistant that can plan trips.",
        system_message="You are a helpful assistant that can suggest a travel plan for a user based on their request."
        )

    local_agent = AssistantAgent(
        name="local_agent",
        model_client=model_client,
        description="A local assistant that can suggest local activities or places to visit.",
        system_message="You are a helpful assistant that can suggest authentic and interesting local activities or places to visit for a user."
        )

    language_agent =AssistantAgent(
        name="language_agent",
        model_client=model_client,
        description="A helpful assistant that can provide language tips for a given destination.",
        system_message="You are a helpful assistant that provides tips for language and communication challenges for travelers."
        )

    summary_agent =AssistantAgent(
        name="travel_summary_agent",
        model_client=model_client,
        description="A helpful assistant that can summarize the travel plan.",
        system_message="You are a helpful assistant that integrates all suggestions into a final detailed travel plan. When complete, respond with TERMINATE."
        )

    termination = TextMentionTermination("TERMINATE")
    group_chat = RoundRobinGroupChat(
            [planner_agent, local_agent, language_agent, summary_agent], termination_condition=termination
        )
    await Console(group_chat.run_stream(task="Plan a 3 day trip to China."))

    await model_client.close()


# Run the async function
if __name__ == "__main__":
    asyncio.run(main())