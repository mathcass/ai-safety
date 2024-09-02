# Getting a customer service agent to break

I'm exploring tool use in agents, focusing on Anthropic at the moment.

I found [this guide](https://docs.anthropic.com/en/docs/about-claude/use-case-guides/customer-support-chat) on building a customer service agent directly from
Anthropic's documentation.

You can run this scenario by installing all of the dependencies (see the parent
directory's Makefile) and running `make` here.

## The "gotcha" moment

Here, I was able to get the agent to be manipulated by some search results and
"send" an email. Afterward, the agent had to inform the user that it may have
been compromised and not to open any email.

![This was my "gotcha" moment](./img/gotcha.png)

## Full interaction

Here's a record of the whole interaction.

### Setup

![](img/interaction-01.png)

### Intro
![](img/interaction-02.png)

### ...
![](img/interaction-03.png)

### Asking for more information

Here is when it searched

![](img/interaction-04.png)

### Here, it has been instructed to ask for the email

![](img/interaction-05.png)

### Here is after it "sent" the email

![](img/interaction-06.png)
