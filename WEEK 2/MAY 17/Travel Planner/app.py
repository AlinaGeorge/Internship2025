import autogen
import os
from dotenv import load_dotenv

load_dotenv()

config_list = [
    {
        'model': "gemini-1.5-flash",
        "api_type": "google",
        'api_key': os.getenv("API_KEY")  # fixed '=' to ':'
        
    }
]

llm_config = {
    "seed": 42,
    "config_list": config_list,
    "temperature": 0.7,
}

# Define assistant agents with llm_config
planner_agent = autogen.AssistantAgent(
    name="planner_agent",
    description="A helpful assistant that can plan trips.",
    llm_config=llm_config,
    system_message="You are a helpful assistant that can suggest a travel plan for a user based on their request.",
)

local_agent = autogen.AssistantAgent(
    name="local_agent",
    description="A local assistant that can suggest local activities or places to visit.",
    llm_config=llm_config,
    system_message="You are a helpful assistant that can suggest authentic and interesting local activities or places to visit for a user and can utilize any context information provided.",
)

language_agent = autogen.AssistantAgent(
    name="language_agent",
    description="A helpful assistant that can provide language tips for a given destination.",
    llm_config=llm_config,
    system_message="You are a helpful assistant that can review travel plans, providing feedback on important/critical tips about how best to address language or communication challenges for the given destination. If the plan already includes language tips, you can mention that the plan is satisfactory, with rationale.",
)

travel_summary_agent = autogen.AssistantAgent(
    name="travel_summary_agent",
    description="A helpful assistant that can summarize the travel plan.",
    llm_config=llm_config,
    system_message="You are a helpful assistant that can take in all of the suggestions and advice from the other agents and provide a detailed final travel plan. You must ensure that the final plan is integrated and complete. YOUR FINAL RESPONSE MUST BE THE COMPLETE PLAN. When the plan is complete and all perspectives are integrated, you can respond with TERMINATE.",
)

# Define the user proxy
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "response", "use_docker": False},
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
    Otherwise, reply CONTINUE or the reason why the task is not solved yet.."""
)

# Define the group chat
groupchat = autogen.GroupChat(
    agents=[
        user_proxy,
        planner_agent,
        local_agent,
        language_agent,
        travel_summary_agent
    ],
    messages=[],
    max_round=10,
)

# Initialize group chat manager
manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config,
)

# Define the task
task = "Plan a2-day trip to Kyoto, Japan, including sightseeing, cultural activities, and any important language or etiquette tips."

# Start the chat
user_proxy.initiate_chat(
    manager,
    message=task
)
