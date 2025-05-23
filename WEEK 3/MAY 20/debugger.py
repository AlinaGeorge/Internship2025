import asyncio
import os
import subprocess
import tempfile
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient


# Tool 1: Python Executor
async def execute_python(code: str) -> str:
    try:
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".py", delete=False) as f:
            f.write(code)
            f.flush()
            result = subprocess.run(
                ["python", f.name],
                capture_output=True,
                text=True,
                timeout=10
            )
        return f"Output:\n{result.stdout}\nErrors:\n{result.stderr}"
    except Exception as e:
        return f"Execution Error: {str(e)}"


# Tool 2: Linter using pylint
async def lint_python(code: str) -> str:
    try:
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".py", delete=False) as f:
            f.write(code)
            f.flush()
            result = subprocess.run(
                ["pylint", f.name, "--disable=all", "--enable=errors,warnings"],
                capture_output=True,
                text=True,
                timeout=10
            )
        return result.stdout
    except Exception as e:
        return f"Linter Error: {str(e)}"


async def main():
    # Create Gemini model client
    model_client = OpenAIChatCompletionClient(
        model="gemini-1.5-flash-8b",
        api_key=os.getenv("API_KEY"),
    )

    # Coder Agent: Generates initial Python code
    coder_agent = AssistantAgent(
        name="coder_agent",
        model_client=model_client,
        description="An agent that writes Python code based on the task description.",
        system_message="You write clean, functional Python code. Use the Python Executor to test your code. Pass it to the Debugger for linting and error fixing.",
        tools=[execute_python],
    )

    # Debugger Agent: Identifies and fixes issues using linting and execution
    debugger_agent = AssistantAgent(
        name="debugger_agent",
        model_client=model_client,
        description="An agent that identifies and fixes errors in Python code.",
        system_message="You use linting and error output to fix Python code. Use the Linter and Python Executor tools to test and debug. Once the code is clean and functional, say TERMINATE.",
        tools=[lint_python, execute_python],
    )

    # Define termination condition
    termination = TextMentionTermination("TERMINATE")

    # Create group chat with Coder and Debugger
    group_chat = RoundRobinGroupChat(
        [coder_agent, debugger_agent],
        termination_condition=termination,
    )

    # Run the collaborative debugging session
    await Console(group_chat.run_stream(task="Write a Python function to check if a number is prime."))

    # Close the model client
    await model_client.close()


# Run the async program
if __name__ == "__main__":
    asyncio.run(main())
