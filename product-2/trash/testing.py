import os
import json
from autogen import UserProxyAgent, AssistantAgent, GroupChat
from autogen.agentchat.contrib.capabilities.teachability import Teachability

# Config for GPT-4
llm_config = {
    "config_list": [
        {
            "model": "gpt-4",
            "api_key": os.getenv("OPENAI_API_KEY")
        }
    ],
    "timeout": 120
}

# Create agents
user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    code_execution_config=False  # no code execution needed here
)

teachable_agent = AssistantAgent(
    name="teachable_agent",
    llm_config=llm_config,
    human_input_mode="NEVER",
    system_message="You are an assistant agent whose only purpose is to summarize data."
)

# Add teachability to the assistant
Teachability().add_to_agent(teachable_agent)

# Function to simulate chunked teaching and summarization
def process_json_chunks(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Teach each chunk
    for chunk in data:
        chunk_text = json.dumps(chunk)
        user_proxy.initiate_chat(
            recipient=teachable_agent,
            message=f"Please learn and summarize this information: {chunk_text}",
            silent=True
        )

    # Request a final summary
    result = user_proxy.initiate_chat(
        recipient=teachable_agent,
        message="Please provide a comprehensive summary of all the information you've learned.",
        silent=True
    )

    return result

# Path to your file
file_path = "file_analysis.json"

# Main runner
if __name__ == "__main__":
    result = process_json_chunks(file_path)
    print("Final Summary:\n", result.summary)
