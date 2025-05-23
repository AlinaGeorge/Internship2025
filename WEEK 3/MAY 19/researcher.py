import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import time
import random


async def main():
    # Create the model client
    model_client = OpenAIChatCompletionClient(
        model="gemini-1.5-flash-8b",
        api_key="AIzaSyCojNDEiD2Lhphj_9vRKbSRItedf-PUQ7o",
    )

    # Define the search tool for the Researcher
    def search_web(query: str) -> str:
        query = re.sub(r"\s+", "+", query.strip())
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            time.sleep(random.uniform(10, 15))

            driver.get(f"https://www.google.com/search?q={query}")
            time.sleep(random.uniform(10, 15))
            content = driver.find_element("tag name", "body").text
            time.sleep(20)
            driver.quit()
            return content[:5000]  # Truncate to avoid overwhelming the LLM
        except Exception as e:
            return f"Error during web search: {str(e)}"

    # Researcher Agent: Searches the web for content
    researcher_agent = AssistantAgent(
        name="researcher_agent",
        model_client=model_client,
        description="An agent that searches the web for relevant content.",
        system_message="You are an assistant that uses the search_web tool to fetch content from Google based on the user's query. Pass the results to the Summarizer.",
        tools=[search_web]  # Register the callable function directly
    )

    # Summarizer Agent: Summarizes the web content
    summarizer_agent = AssistantAgent(
        name="summarizer_agent",
        model_client=model_client,
        description="An agent that summarizes web content into concise points.",
        system_message="You are an assistant that summarizes the provided web content into concise points (under 200 words). Pass the summary to the Validator."
    )

    # Validator Agent: Checks the summary for accuracy and length
    validator_agent = AssistantAgent(
        name="validator_agent",
        model_client=model_client,
        description="An agent that validates the summary for accuracy and length.",
        system_message="You are an assistant that checks if the summary is under 200 words and captures key points from the web content. Provide feedback and pass to the Finalizer. If the summary is satisfactory, mention it with rationale."
    )

    # Finalizer Agent: Creates the final polished summary
    finalizer_agent = AssistantAgent(
        name="finalizer_agent",
        model_client=model_client,
        description="An agent that creates the final polished summary.",
        system_message="You are an assistant that takes the validated summary and feedback to produce a final, polished summary. Ensure the summary is complete and integrated. When done, respond with 'TERMINATE'."
    )

    # Set up termination condition
    termination = TextMentionTermination("TERMINATE")

    # Create round-robin group chat
    group_chat = RoundRobinGroupChat(
        [researcher_agent, summarizer_agent, validator_agent, finalizer_agent],
        termination_condition=termination
    )

    # Run the group chat with the task
    await Console(group_chat.run_stream(task="Research latest AI trends."))

    # Close the model client
    await model_client.close()

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())