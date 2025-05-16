import autogen

config_list=[
    {
        'model':"gemini-1.5-flash",
        "api_type": "google",

        'api_key':'AIzaSyCEW5Rt9fiEDITDwTXNeHt_XyeRkCyjTE4'
    }
]

llm_config={
    
    "seed": 42,
    "config_list": config_list,
    "temperature": 0,
}

assistant=autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config,
    )

user_proxy=autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "response",
                            "use_docker": False,},
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
    Otherwise, reply CONTINUE or the reason why the task is not solved yet.."""

)
task= """
Give me a summary of the following text:

"The mitochondria, often referred to as the powerhouse of the cell,
 are critical in energy production through oxidative phosphorylation. 
 Recent studies have shown their role in apoptosis and innate immunity, 
 positioning them as key regulators in cellular homeostasis and disease."

"""

user_proxy.initiate_chat(
    assistant,
    message=task
)