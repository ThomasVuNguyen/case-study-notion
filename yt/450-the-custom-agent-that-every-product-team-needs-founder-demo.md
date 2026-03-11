# The Custom Agent That Every Product Team Needs | Founder Demo

**URL:** [https://www.youtube.com/watch?v=w5cFKe2H3Qw](https://www.youtube.com/watch?v=w5cFKe2H3Qw)
**Date:** 2026-02-24

![The Custom Agent That Every Product Team Needs | Founder Demo](../images/450-the-custom-agent-that-every-product-team-needs-founder-demo.jpg)

## Transcript

**[Voiceover]**

"The goal of the feedback router is just to accept the fact that no one knows what the teams are and who's responsible for what and just let people post bugs in an unstructured way and then just try to magically make a bug a ticket and assign to the right team. Hey, my name is Simon. I'm one of the"

"co-founders of Notion and I've been working on Notion for about 12 and a half years. And these days I sp I spend most of my time uh working on our new AI features. So today I want to show you a custom agent that that we created. This is actually one of the first custom agents that we ever made"

"back when we were developing the feature. It's called notion feedback router. So we have this Slack channel internally called all product feedback chatter and it's sort of a catch-all channel where anyone at the company can post in it about a bug or a piece of product feedback. And we've had this channel for years and it's always been kind"

"of a problem that sort of no one really owns the channel and people sometimes post and it sort of gets lost in in the mix or no one replies and it doesn't get doesn't get to the right team and the bug gets gets fixed and that problem only got worse as as the company got got bigger and there's"

"more and more teams. So the way it works is it's a custom agent and it and it has access uh to this Slack channel by the trigger. So, it's going to be listening to all the messages in the channel and then it uses this routing rules page to decide what to do and and and how to respond. And"

"[music] usually what it does is it will crossost to a different Slack channel and potentially file a bug or a task. So, I'll show you an example. Uh here's one from earlier today. Uh there's there's a bug with a tool tip and uh the feedback router replied, I filed a bug and then it crossosted to this other engineering"

"team channel. So the the really fun part of this though is that no human wrote these writing rules. The way it works actually is we started with a blank page and the agent is is given access itself to learn on the fly where to where to route things. [music] Um and it's and it's told to do that in"

"its instruction. So this this notion page is essentially the agent's memory. And I'll show you an example of that. So here's one from earlier today. uh there is an issue with uh page emojis and you can see here that the feedback router initially replies saying it doesn't have a rule. It doesn't know what to do. So I just"

"replied and said let's file into this team slack channel and then what it did is it it filed a bug, crossosted into the channel and then updated its own routing rules. So you can see here it can learn on the fly just like a person would by just just telling it what to do, giving it feedback. And over"

"the months uh it's accumulated [music] quite a large page with many many different rules which honestly no no human has ever really a read end to end. But that's not really the point. The point is that you know that the agent maintains this itself and solves this problem for us of figuring out where to route feedback so that"

"it gets solved. Okay. Okay. So, if you wanted to make your own feedback router, you would want to make a blank agent. Um, you you would need to uh give it a Slack trigger so that can listen to your your Slack channel where you're going to post your bugs. Then you need to give it access to any uh"

"task database that you use in notion as well as a a blank routing rules page that we use as its uh memory. And and then finally, the last step is just to write some some basic instructions to uh to tell it how you want it to work. And and the really important bit of that is is to tell"

"it that it should use its routing rules page to decide what to do and that if it's given feedback, it should update its own routing rules page to improve its behavior in the future. And then beyond that, you know, you can start adding more specific rules if you wanted to if you want to constrain it behavior further. But"

"but that's just sort of get you started in in in the basic setup."

