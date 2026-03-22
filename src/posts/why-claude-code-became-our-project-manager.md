---
title: "Why Claude Code Became Our Project Manager"
date: "2026-03-22"
description: "We started using Claude Code to help write code. What surprised us was how useful it became for project management. Because it can read the repo, issues, PRs, and milestones together, it often sees the project more holistically than any one engineer can. That makes it good not just at tracking work, but at spotting gaps, prioritizing what matters, and reframing local tickets as the real problems behind them."
slug: "why-claude-code-became-our-project-manager"
---
# Why Claude Code Became Our Project Manager

We started using Claude Code for coding. Over time, one of its most valuable roles turned out to be project management.

The reason is simple: in a large enough codebase, **no single human fully holds all the relevant context**. People understand their own area, maybe a few adjacent systems, and some recent decisions. But the true state of a project lives across code, PRs, issues, docs, conventions, and a long tail of half-written assumptions. Traditional project management artifacts are only compressed summaries of that reality. As the codebase grows, those summaries drift.

Claude Code can read the codebase directly and reason over it alongside GitHub. That matters more than it sounds. Most PM pain in engineering is **not** about tracking tasks. It is about maintaining an **accurate picture of reality**.

---

## The Core Idea

It turns out you do **not** need another dashboard. **GitHub already has the right primitives**: milestones, issues, and PRs.

The missing piece was an agent that can operate across them while staying grounded in the actual repository.

But you have to use those primitives correctly.

### **Milestones**
A **milestone** should define **what needs to be achieved** at a given stage.

In our case, milestones are usually monthly and should be as concrete as possible. The more clearly a milestone describes the capability we want by the end of the month, the more useful Claude becomes. It can read the codebase, compare the current system against the milestone, and identify what is still missing.

### **Issues**
An **issue** should define **what problem needs to be addressed**, not how to solve it.

This is one of the biggest mindset shifts. If issues are framed as todos or implementation plans, they prematurely lock in a local solution. In a complex system, that often leads to suboptimal decomposition.

Claude is most useful when it is asked to reason from the problem: what is missing, what is blocking progress, and what the best next step is given the full codebase context. The **PR** is where the how belongs.

### **Labels**
Do not bother with rigid hierarchies like GitHub Projects. Work never partitions that cleanly.

Use **labels** instead. They are flexible, and Claude can group them dynamically without forcing you to maintain a fake tree structure.

---

## What This Unlocks

In practice, this gives us **three new superpowers**.

### Prioritizing Work Against a Milestone

One common workflow is prioritizing my own issues.

I can give Claude the current milestone and my open issues and ask **what I should do first**. It usually does a better job than a quick human pass because it is not just looking at ticket titles. It can inspect the code, understand what is already partially implemented, notice dependencies, and judge which issues most directly move the milestone forward.

It is also useful in waiting states. If a PR is under review, I can ask for the best **decoupled task** to work on next instead of context-switching blindly.

![Claude prioritizing personal issues against a milestone](/images/posts/claude-pm-prioritizing.png)
*Screenshots have been anonymized by Gemini and do not reflect real work content.*

### Evaluating Real Progress

Another useful workflow is answering the classic Elon question: **“What have you done last week?”**

The interesting part is not the summary itself. Any tool can list merged PRs and closed issues. What matters is whether that activity actually **advanced the milestone**.

Claude can look at recent work and tell you whether the project is moving at a reasonable pace, whether the work is concentrated on the critical path, and whether the apparent progress is real or just activity.

That is a much better management question than simply asking **what changed**.

![Claude summarizing last week’s work and evaluating progress](/images/posts/claude-pm-progress.png)
*Screenshots have been anonymized by Gemini and do not reflect real work content.*

### Milestone Gap Analysis

The third workflow we use a lot is **milestone gap analysis**.

We ask Claude: **given the current codebase, how far are we from this milestone?**

This is where the code-grounded nature of the workflow matters most. Claude can identify:

- Capabilities that are already present
- Capabilities that are only partially implemented
- Gaps that are not even clearly represented in the issue tracker

Sometimes the code suggests that a milestone is closer than the issue list implies. Other times the opposite is true: several issues are closed, but the end-to-end capability is still not really there because integration, testing, or edge cases are missing.

## The Deeper Lesson

The atomic unit of project management should **not** be a todo item. It should be **a problem**.

A todo assumes the decomposition is already correct. In large codebases, that assumption is often wrong. Engineers naturally reason locally because they only see a slice of the system. Claude, with access to broader context, can sometimes suggest a better decomposition or a more globally optimal solution than a human would arrive at from within one module or team boundary.

That does **not** mean Claude invents strategy. It does not.

This only works when humans provide **clear high-level goals and milestones**. If the team has not decided what it is trying to achieve, Claude cannot manufacture that context out of thin air. It is much better at **operationalizing strategy** than creating it.

Its strength is in taking a defined goal, mapping it onto the current codebase, identifying gaps, surfacing dependencies, and helping decide what matters most next.

---

## What Teams Need First

There is another important prerequisite: teams need to write down their previously unsaid context.

Files like **CLAUDE.md**, **README.md**, and lightweight design docs matter a lot. Claude is powerful, but it is not magic. It can only consume context that exists in some explicit form.

Teams that rely heavily on oral tradition or long-tenured engineers carrying unwritten assumptions in their heads will get much less value out of this workflow.

If you give Claude a **clear goal** and **explicit context**, it does something profound:

It shifts project management from **tracking tasks** to **managing context**, grounded in the only thing that is actually real:

**the code.**