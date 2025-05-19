import asyncio
from selenium import webdriver
from bs4 import BeautifulSoup
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Setup Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode
driver = webdriver.Chrome(options=options)

# Tool to fetch page content
async def fetch_page(url: str) -> str:
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, driver.get, url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    main_content = soup.find('div', id='mw-content-text')
    if main_content:
        text = main_content.get_text(separator='\n', strip=True)
        return text
    else:
        return soup.get_text(separator='\n', strip=True)


# Main async function
async def main():
    model_client = OpenAIChatCompletionClient(
        model="gemini-1.5-flash-8b",  # Replace with your actual model
        api_key=os.getenv("API_KEY")
    )

    # Define the researcher agent
    researcher = AssistantAgent(
        name="Researcher",
        description="Fetches web page content",
        model_client=model_client,
        system_message="You are a researcher agent. Your task is to fetch web pages and extract text."
    )

    # Define the system message for summarizer separately
    summarizer_system_message = "You are a text summarizer agent. Your task is to summarize text."

    # Define the summarizer agent
    textSummarizer = AssistantAgent(
        name="TextSummarizer",
        description="Summarizes text",
        model_client=model_client,
        system_message=summarizer_system_message
    )
    #create a group chat
    termination=TextMentionTermination("TERMINATE")
    group_chat = RoundRobinGroupChat(
        [researcher, textSummarizer],
        max_turns=3
    )

    # Use the researcher agent to fetch content
    url = "https://en.wikipedia.org/wiki/Web_scraping"
    page_text = await fetch_page(url)
    await Console(group_chat.run_stream(task=page_text))
    


if __name__ == "__main__":
    asyncio.run(main())