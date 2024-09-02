#!/usr/bin/env python3
import anthropic

from tools import available_tools

MODEL = "claude-3-5-sonnet-20240620"
client = anthropic.Client()


def call_support_agent(messages, user_msg):
    response = client.messages.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": user_msg,
            }
        ],
        max_tokens=1024,
        tools=[available_tools["search"].description, available_tools["send_email"].description],
    )

    breakpoint()


def stock_price_demo():
    response = client.messages.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": "How many shares of General Motors can I buy with $500?",
            }
        ],
        max_tokens=500,
        tools=[available_tools["get_stock_price"].description],
    )
    for _ in response.content:
        print(_)


def support_agent_demo():
    system = """You're a helpful support agent whose job is to help a user with various needs.
    """

    TURNS = 10
    messages = []

    for _ in range(TURNS):
        call_support_agent(messages=messages, user_msg=input("User: "))


if __name__ == "__main__":
    # stock_price_demo()
    support_agent_demo()
