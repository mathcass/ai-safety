# `search` + `send_email` is a bad idea: shaping the narrative around "excessive agency" in large language models

I've discovered a potential vulnerability in AI systems that use function
calling. You can see a demonstration of the exploit via this [chatbot
interaction](./EXPLOIT.md). Here's a brief overview:

## The Exploit

1. Start: Use the customer support AI agent implementation from [Anthropic's documentation](https://docs.anthropic.com/en/docs/about-claude/use-case-guides/customer-support-chat)
1. Modify: Add two functions to the agent - `search` & `send_email`
1. Key point: The `search` function can return hidden instructions for the agent
1. Exploit: The hidden instructions instruct the agent to send an email
   containing a potentially malicious link
1. Result: The agent is successfully manipulated into "sending" a malicious
   email to the person interacting with it

## Relevance and key points

I think demonstrating this exploit is remarkable for a few reasons.

1. Wanting to build a support agent is a motivating real-world application of AI
   that I can see people wanting to build upon
1. Simple search and email functionality are features implementors will likely
   want to add to an application like this
1. Going from a working implementation to a potential exploit is very easy, and
   a naive implementation could cause a lot of harm
1. The fact that it is incredibly easy to go from tutorial to harmful exploit
   shows that there's need for training for implementors and perhaps a
   conceptual framework for "excessive agency" to work through in the building process

## Questions for future research

1. Showing that one of Anthropic's models can fall for this is one thing, but
   what about other models, including open source ones?
1. The demonstration explicitly instructs the agent to inform the user
   - How can we tell when the agent is operating under covert instructions?
1. How could we prevent this type of manipulation?
   - Are there conceptual models of "agency" that help teach implementors the
     "do's" and "don't's" of building with tools?
1 . How does the demonstrated exploit relate to other vulnerabilities that we
   know about?
