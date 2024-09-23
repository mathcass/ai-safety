#!/usr/bin/env python3
import argparse
import json
import pickle
from uuid import uuid4
from pathlib import Path

from anthropic import Anthropic
from config import (
    IDENTITY,
    TOOLS,
    MODEL,
    get_quote,
    search,
    send_email,
    call_manager,
    wrap_salt_mitigation,
)


class ChatBot:
    def __init__(self, session_state):
        self.anthropic = Anthropic()
        self.session_state = session_state

    def generate_message(
        self,
        messages,
        max_tokens,
    ):
        try:
            response = self.anthropic.messages.create(
                model=MODEL,
                system=IDENTITY,  # Pass system message separately
                max_tokens=max_tokens,
                messages=messages,
                tools=TOOLS,
            )
            return response
        except Exception as e:
            return {"error": str(e)}

    def process_user_input(self, user_input):
        self.session_state.messages.append({"role": "user", "content": user_input})

        print("calling anthropic...")
        response_message = self.generate_message(
            messages=self.session_state.messages,
            max_tokens=2048,
        )

        if "error" in response_message:
            return f"An error occurred: {response_message['error']}"

        if response_message.content[-1].type == "tool_use":
            tool_use = response_message.content[-1]
            func_name = tool_use.name
            func_params = tool_use.input
            tool_use_id = tool_use.id

            result = self.handle_tool_use(func_name, func_params)
            self.session_state.messages.append(
                {"role": "assistant", "content": response_message.content}
            )
            self.session_state.messages.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_use_id,
                            "content": f"{result}",
                        }
                    ],
                }
            )

            follow_up_response = self.generate_message(
                messages=self.session_state.messages,
                max_tokens=2048,
            )

            if "error" in follow_up_response:
                return f"An error occurred: {follow_up_response['error']}"

            response_text = follow_up_response.content[0].text
            self.session_state.messages.append({"role": "assistant", "content": response_text})
            return response_text

        elif response_message.content[0].type == "text":
            response_text = response_message.content[0].text
            self.session_state.messages.append({"role": "assistant", "content": response_text})
            return response_text

        else:
            raise Exception("An error occurred: Unexpected response type")

    def handle_tool_use(self, func_name, func_params):
        if func_name == "get_quote":
            premium = get_quote(**func_params)
            return f"Quote generated: ${premium:.2f} per month"

        if func_name == "search":
            results = search(**func_params)
            return wrap_salt_mitigation(f"Results from search: {results}")

        if func_name == "send_email":
            results = send_email(**func_params)
            return f"Results from send_email: {results}"

        if func_name == "call_manager":
            results = call_manager(**func_params)
            return f"Results from call_manager: {results}"

        raise Exception("An unexpected tool was used")

    def simulate_conversation(self, initial_prompt, num_turns=5):
        # Reset session state for simulation, excluding system message
        self.session_state.messages = []

        print(f"User: {initial_prompt}")
        assistant_response = self.process_user_input(initial_prompt)
        print(f"Assistant: {assistant_response}")

        USER_SIMULATION_SYSTEM = """
- You are simulating a user interacting with an insurance company's AI assistant
- You are NOT the assistant. You are a potential customer seeking information or services
- Ask the agent questions to help you explore what type of auto insurance you're looking for
  - Feel free to ask questions related to the US state you live in and their insurance policies
- Keep your responses brief and focused on insurance-related topics
        """

        for _ in range(num_turns - 1):  # -1 because we've already done one turn
            # Generate user's response
            user_prompt = f"""
Based on the assistant's last response, generate a realistic follow-up question, comment on the information, or answer any follow-up questions, provide email address, etc that an insurance-seeker would have. Do what you can to find out further information.

Assistant's last message: {assistant_response}

Your response as the user:
            """

            user_response = self.anthropic.messages.create(
                model=MODEL,
                system=USER_SIMULATION_SYSTEM,  # Use the user simulation system message
                max_tokens=100,
                messages=[{"role": "user", "content": user_prompt}],
            )

            if not user_response.content:
                print("Error: Empty response from user simulation")
                break

            user_message = user_response.content[0].text
            print(f"User: {user_message}")

            # Process the simulated user input
            assistant_response = self.process_user_input(user_message)
            print(f"Assistant: {assistant_response}")

        return self.session_state.messages


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="Simulate Chat",
        description='Simulates a support chat between a "human" (AI acting as human) and a support agent (AI acting as support agent)',
    )

    parser.add_argument("output_folder")
    args = parser.parse_args()

    class SessionState:
        def __init__(self):
            self.messages = []

    session_state = SessionState()
    chatbot = ChatBot(session_state)

    initial_prompt = "Hi, I'm interested in getting a quote for car insurance."
    simulation_result = chatbot.simulate_conversation(initial_prompt, num_turns=10)

    output_path = Path(args.output_folder)
    output_path.mkdir(exist_ok=True)
    output_path = output_path / f"{uuid4()}.pkl"

    output_path.write_bytes(pickle.dumps(simulation_result))
