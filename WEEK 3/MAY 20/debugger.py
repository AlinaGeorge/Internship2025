'''import asyncio
import os
import subprocess
import tempfile
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
#from autogen_agentchat.tools import Tool
from autogen import Tool


from dotenv import load_dotenv

load_dotenv()

# --- Tool: Linter using pylint ---
def lint_code(code: str) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode='w') as f:
        f.write(code)
        temp_file_path = f.name

    result = subprocess.run(
        ["pylint", temp_file_path, "--disable=all", "--enable=E,F,W,C"],
        capture_output=True,
        text=True
    )
    os.unlink(temp_file_path)
    return result.stdout

# --- Tool: Python Executor ---
def run_python_code(code: str) -> str:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode='w') as f:
            f.write(code)
            temp_file_path = f.name
        result = subprocess.run(["python", temp_file_path], capture_output=True, text=True, timeout=10)
        os.unlink(temp_file_path)
        if result.returncode != 0:
            return f"❌ Error:\n{result.stderr}"
        return f"✅ Output:\n{result.stdout}"
    except subprocess.TimeoutExpired:
        return "⏰ Execution timed out"

# --- Setup Gemini Wrapper ---
model_client = OpenAIChatCompletionClient(
    model="gemini-1.5-flash-8b",  # Or your deployed model name
    api_key=os.getenv("API_KEY")
)

# --- Define Agents ---
coder = AssistantAgent(
    name="Coder",
    description="Writes Python code from a user request.",
    model_client=model_client,
    system_message="You are a helpful agent that writes Python code based on user input."
)
lint_tool = Tool(name="LintCode", func=lint_code, description="Lints Python code using pylint.")
exec_tool = Tool(name="RunCode", func=run_python_code, description="Runs Python code and returns output.")

debugger = AssistantAgent(
    name="Debugger",
    description="Runs linting and execution to debug the code.",
    model_client=model_client,
    system_message=(
        "You are a debugging assistant. You run `pylint` on the code and execute it. "
        "Then give suggestions for improvements if any errors or warnings occur."
    ),
    tools=[lint_tool, exec_tool]  # ✅ This is now a valid list of Tool objects
)




# --- Main Async Execution ---
async def main():
    group_chat = RoundRobinGroupChat(
        agents=[coder, debugger],
        max_rounds=5,
        messages=[],
        termination=TextMentionTermination("TERMINATE")
    )

    task = """Write a Python program that accepts a list of numbers and returns their median.
Make sure to handle both even and odd cases. Then run it with the input [3, 5, 1, 9, 7]."""
    
    await Console(group_chat.run_stream(task=task))

if __name__ == "__main__":
    asyncio.run(main())'''


#creating two agents coder and debugger
#coder will generate code and debugger will debug the code
#debugger will use pylint to debug the code
#coder will use gemini to generate code
#debugger will use gemini to debug the code
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from pylint.lint import Run


load_dotenv()
# Load environment variables from .env file
async def main():
    model_client = OpenAIChatCompletionClient (
        model="gemini-1.5-flash-8b",
        api_key=os.getenv("API_KEY") # Load from .env
)

#define the coder agent
    coder = AssistantAgent(
        name="Coder",
        model_client=model_client,
        description="Code generation agent",
        system_message="You are a helpful coding assistant.",
    )

    # Define the debugger agent
    debugger = AssistantAgent(
        name="Debugger",
        model_client=model_client,
        description="You are a helpful debugging assistant.",
        system_message="You are a helpful debugging assistant when done debugging type Terminate.",
        
    )
    termination_condition=TextMentionTermination("Terminate")
    # Create a group chat with round-robin communication
    group_chat = RoundRobinGroupChat([coder, debugger],termination_condition=termination_condition)

    # Create a console UI for the group chat
    t=input("Enter the program to generate code for: ")
    await Console(group_chat.run_stream(task=t))

    await model_client.close()
# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
