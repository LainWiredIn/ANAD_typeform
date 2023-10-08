import openai
import pandas as pd
openai.api_key = "YOUR_OPENAI_API_KEY"

def chat_with_agents():
    user_details = {}
    
    # Initializing agents with specific roles
    agents = {
        "convincing_agent": "You are an assistant that convinces the user to provide information.",
        "info_extraction_agent": "You are an agent that extracts and verifies user information.",
        "formatting_agent": "You are an agent that formats the extracted information."
    }

    # Initializing a conversation with the convincing agent
    conversation = [
        {"role": "system", "content": "You are chatting with multiple agents."},
        {"role": "convincing_agent", "content": agents["convincing_agent"]}
    ]

    while True:
        response = openai.ChatCompletion.create(
            # can choose different models, like curie or davinci
            model="gpt-3.5-turbo",
            messages=conversation
        )
        
        # Extract the message from the agent's response
        agent_message = response['choices'][0]['message']['content']
        
        # Add the agent's message to the conversation
        conversation.append({"role": "user", "content": agent_message})

        # need to add explicit "info_extraction_agent" conversation
        
        # Check if the user provided the information and extract it
        if "Name:" in agent_message:
            user_details["Name"] = agent_message.replace("Name:", "").strip()
        
        if "Email:" in agent_message:
            user_details["Email"] = agent_message.replace("Email:", "").strip()

        if "Phone:" in agent_message:
            user_details["Phone"] = agent_message.replace("Phone:", "").strip()

        if "Address:" in agent_message:
            user_details["Address"] = agent_message.replace("Address:", "").strip()

        if "Date of Birth:" in agent_message:
            user_details["Date of Birth"] = agent_message.replace("Date of Birth:", "").strip()

        if "Education:" in agent_message:
            user_details["Education"] = agent_message.replace("Education:", "").strip()

        # Check if user provided all details
        if all(detail in user_details for detail in ["Name", "Email", "Phone", "Address", "Date of Birth", "Education"]):
            break
    
    # Initialize a conversation with the formatting agent
    conversation = [
        {"role": "system", "content": "You are chatting with multiple agents."},
        {"role": "formatting_agent", "content": agents["formatting_agent"]}
    ]

    # Format extracted information
    for key, value in user_details.items():
        conversation.append({"role": "user", "content": f"{key}: {value}"})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )

    # Save the user details to a CSV file
    user_data = pd.DataFrame.from_dict(user_details, orient='index', columns=['Value'])
    user_data.to_csv("user_details.csv")

if __name__ == "__main__":
    chat_with_agents()
