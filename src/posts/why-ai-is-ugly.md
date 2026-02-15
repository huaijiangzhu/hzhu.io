---
title: "Why AI is Ugly"
date: "2026-02-15"
description: "Recently, there is an argument that in the post-AGI era, taste will be the ultimate differentiator: because when anyone can build anything, only taste sets you apart. I suspect this is merely our inflated sense of self-importance as human beings."
slug: "why-ai-is-ugly"
---
# Why AI is Ugly

**Because it's smarter than you.**

Last Friday, I caught myself doing something strange: I was arguing with a ghost. I was using Claude Code to create a new feature. The agent spat out a Python script that was functional, bug-free, and passed every test case—that it wrote itself—on the first try. It worked. But I couldn't leave it alone.

I spent the next twenty minutes renaming variables, restructuring the class hierarchy, and adjusting the whitespace.

I told myself I was optimizing for readability. I was imposing *taste*.

But then I realized what I was actually doing. I was applying human aesthetics to something that no longer required human attention. The code didn't need to be tasteful; it just needed to be correct. This script will likely be maintained, refactored, and eventually deprecated by another AI. My insistence on elegance and clean code wasn't a universal truth. Humans need clean code because our working memory is small. We need structure to understand logic. We are single-threaded processors with very limited RAM.

To an AI, my *good taste* is just inefficient formatting. Today's coding agents are trained via reinforcement learning: they generate solutions and are rewarded on whether the tests pass. Taste is being selected against whenever it doesn't contribute to functional correctness.

This realization is uncomfortable because it strikes at the heart of what we consider *Good Design*. In [Taste for Makers](https://paulgraham.com/taste.html), Paul Graham argued that taste is objective, timeless, and universal. But Graham's argument rested on a hidden premise: that the consumer of design is a human being.

## The Bandwidth Problem

For the last forty years, software design has been dominated by a single bottleneck: Human-Computer Interaction. We built GUIs, icons, and metaphors—files, folders, desktops—to bridge the gap between computers and our brains.

Consider *flow*. We praise designs that lead users effortlessly from step A to step B. But flow is a solution to a specific problem: humans process information sequentially. We can only focus on one thing at a time, so we need a narrative.

An AI agent has no such constraint. It doesn't *navigate* a checkout process or *browse* a catalog. It has random access to the entire data structure. The flow is an arbitrary throttle on speed.

We prize minimalism because complexity overwhelms us. We need whitespace. We need clean abstractions. But AI thrives on density. A JSON response containing 5,000 parameters looks ugly to a human, but to an AI, it is just what it needs.

## The Retreat from the GUI

You can see the shift happening already.

A year ago, the cutting edge of AI-assisted development was Cursor. But lately, the most advanced developers are abandoning GUIs for tools like Claude Code: Terminal User Interfaces (TUIs).

The reason is simple. A GUI is a bottleneck. In Cursor, if I want to refactor a module, I have to find the button or remember the hotkey to toggle on the agent mode. The designer decided how I should solve the problem. In a terminal, I just type: *Refactor this module.*

The GUI assumes the user needs guidance. The terminal assumes the user has intent.

This retreat from designed interfaces doesn't just apply to developers. It will extend to everyone.

There is an economic argument for why we value taste, and specifically *timeless* design. Graham suggests we should avoid trends and build things that last. But this is largely a constraint of manufacturing costs. In the physical world, and even in the pre-AGI software world, building a high-quality interface was expensive. You couldn't afford to redesign your app every time a user opened it, so you aimed for a timeless design that would remain acceptable for years.

But what happens when the marginal cost of generating an interface drops to zero?

We are approaching what you might call Just-in-Time (JIT) Interfaces. Imagine every interaction with a device begins by stating an intent. The system generates an interface on the fly: shaped not by a designer, but by *you*. Your stress level, your available time, your environment, your history.

When the task is done, the interface is destroyed.

This collapses the entire logic of timeless design. A timeless artifact makes sense when you're amortizing production costs over a long shelf life. But a disposable interface has no shelf life: It doesn't need to be timeless, it just needs to be *timely*.

## The Taste of the Machine

This leads to the most uncomfortable conclusion.

When you design a *tasteful* product, you are making a decision for the user. You are saying: *I know how you should solve this problem.* You are imposing your preference–or your guess at the average user's preference–on every individual. In the pre-AGI era, it was impossible to create a unique product for every user, so we designed a single generic one and forced everyone to adapt to it. Taste was a necessary tyranny of scale.

In the post-AGI era, this imposition is just arrogance. It is condescending to assume you know the optimal way for a stranger to solve their problem, when the machine could just ask them and generate a solution in milliseconds.

What we call *objectivity* in design was only ever consensus: an agreement on what the average human finds pleasing. And if AI agents are already being optimized away from human aesthetics, they may eventually converge on their own sense of *good*. Not beauty, but whatever structural properties make content most amenable to machine comprehension, modification, and generation. A machine taste we won't be able to perceive. To the human eye, perfect machine code will look indistinguishable from random noise.

*Taste* was never a fundamental property of the universe. It was a compression algorithm. We used it to simplify complex reality into something our limited brains could process. We used *good design* to ration our scarce attention.

To the AI, there is no scarcity of attention, so there is no need for compression.

What Graham called *Good Design* was really *Human Design*. And the ghost I was arguing with doesn't read like a human anymore. I'm not sure it ever needed to.