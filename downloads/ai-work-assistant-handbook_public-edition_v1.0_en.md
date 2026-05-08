# AI Work Assistant Handbook

> Build repeatable AI workflows: assign clearly, verify output, refine results, and save what works.

---

## Handbook Information

| Field | Details |
| --- | --- |
| Edition | Free Public Edition v1.0 |
| Last Updated | 2026-05-08 |
| Author | Farceur Liu |
| Audience | First-time AI users in professional settings; individuals, small teams, and managers looking to integrate AI into daily work |
| Core Theme | Start with one low-risk task, then build a personal system for assigning work to AI, verifying output, refining results, and saving what works |
| Suggested Use | Self-study, team onboarding, workflow documentation, skill design |
| Not Suitable For | Replacing legal, financial, security, medical, or HR decisions |

---

## About This Handbook

Most people who start using AI ask the same first question: "Is there a better tool?"

But the real obstacle is rarely the tool. It is usually the process: not knowing how to delegate clearly, how to provide the right context, how to stop AI from guessing, how to review the first draft, or how to save a useful method so it can be reused.

The core argument of this handbook is simple: you do not need many AI tools. One or two mainstream tools are almost always enough. The real gap is not the tool list - it is the working method.

This handbook starts with one low-risk task and walks you through turning AI from a chat partner into a work assistant you can actually delegate to. You will learn how to choose tasks, write clear assignments, read for errors, ask for revisions, save templates, and decide when a workflow is worth packaging as a skill.

---

## A Note on the Original Title

The original Chinese version of this handbook is titled: "從零開始養成我的 AI 管家." A rough translation would be "Building My AI Butler from Scratch." The word "butler" in that title evokes the idea of a trusted assistant who learns your preferences, handles repeatable tasks, and follows standing instructions - but never makes final decisions on your behalf.

This English edition uses "AI work assistant" instead. The idea is the same: you are not trying to find the perfect tool or automate everything at once. You are building a working relationship with AI - teaching it your context, setting clear boundaries, and gradually turning reliable methods into reusable systems.

---

## Public Disclaimer and Permissions

This handbook provides general guidance on AI work methods and safety principles. It does not constitute legal, financial, security, medical, or HR advice. When working with company data, customer data, personal information, financial transactions, contracts, account permissions, system operations, script execution, or file deletion, you must follow your organization's policies, authorization scope, and IT or security guidelines.

Do not use examples from this handbook to bypass organizational policies, install unknown tools, run scripts you do not understand, or process unauthorized data. Tool names, interfaces, and features change over time - refer to official product documentation and your organization's policies for current guidance.

The product names ChatGPT, Claude, Gemini, Codex, Claude Code, Gemini CLI, and others mentioned in this handbook are the property of their respective owners. This handbook does not represent any affiliation, authorization, endorsement, or guarantee relationship with those tools, platforms, or companies.

**Permissions:** This handbook may be freely read and shared via its original link. Without explicit written permission from the author, the full text or substantially adapted content may not be resold as commercial courses, paid training materials, publications, consulting deliverables, or enterprise training content. When quoting excerpts, please include the handbook title and source link: https://farceurliu.github.io/ai-butler-handbook/

---

## Before You Begin: Organizational Policies vs. This Handbook

This handbook is a public self-study resource. Its focus is teaching you how to turn AI from a chat tool into a delegatable, verifiable, and accumulating work assistant.

It is not a formal AI usage policy for any company, school, client, or organization. It does not define your approved tools, data classification rules, account permissions, security reporting procedures, legal processes, or financial rules.

Three principles to keep in mind:

1. Methods can be self-studied; data boundaries depend on your organization's rules.
2. Tools can be practiced; formal data and system permissions depend on your authorization.
3. AI can help organize and draft content, but it cannot replace formal decisions, commitments, approvals, or reporting workflows.

If anything in this handbook conflicts with your organization's formal policies, follow your organization's policies.

---

## Table of Contents

- Handbook Information
- About This Handbook
- Public Disclaimer and Permissions

Main Chapters:
- 0. How to Use This Handbook
- 1. What an AI Work Assistant Is, and Is Not
- 2. Your First Low-Risk Assignment
- 3. Beginner No-Go Zones
- 4. Tools, Chat, Workspace AI, CLI Agents, and Skills
- 5. Choosing the Right Tasks
- 6. The Assignment Formula
- 7. Practice Loops
- 8. Everyday Workflow Scenarios
- 9. Diagnosing Bad Assignments
- 10. Verification: Do Not Accept Output Blindly
- 11. Refinement: Make the Second Version Useful
- 12. Safety Boundaries
- 13. Assignment Quality Levels
- 14. Confidence Labels
- 15. Pre-Send Checklist for External Replies
- 16. Template Library
- 17. Red-Flag Rules
- 18. Turning Reusable Workflows into Skills
- 19. Team Adoption and Knowledge Capture
- 20. One-Page Quick Reference
- 21. Closing

Appendices:
- Appendix A: High-Risk Customer Message Triage
- Appendix B: Expense Reimbursement Completeness Check
- Appendix C: Email Search and Attachment Safety Check
- Appendix D: Safe Computer Storage Cleanup

---

## 0. How to Use This Handbook

**What you will learn in this chapter:**
- Understand the learning path and recommended reading order.
- Know that building an AI work assistant is not a one-time setup, but a cycle of assigning, verifying, refining, and saving.
- Establish the core principle: fewer tools, deeper method.

"Building" an AI work assistant does not mean giving it a personality or a name. It means gradually teaching it your working context until it can reliably handle repeatable tasks:

1. Get it to complete one low-risk task.
2. Review its first attempt.
3. Point out problems and ask for a revision.
4. Save the useful method as a template.
5. Repeat until you can package a stable workflow as a skill.

### 0.1 If this is your first time using AI as a work tool

Read in this order:
1. Chapter 1: Understand the responsibility boundary
2. Chapter 2: Complete your first low-risk task
3. Chapter 6: Learn the assignment formula
4. Chapter 7: Complete the three practice loops
5. Chapter 10: Use the verification checklist

Your goal the first time is not a perfect output. It is completing one cycle:

> Assign once -> Review the first version -> Find the problem -> Ask for a revision -> Get a more usable second version.

### 0.2 If you just want templates

Go directly to Chapters 8, 16, and 20. But do not copy-paste without adapting. At minimum, add:
- The goal for this specific task
- The data AI can refer to
- What AI must not assume, commit to, or modify

### 0.3 Reader path table

| Your situation | Recommended path | What you should be able to do after |
| --- | --- | --- |
| First-time AI user | Chapters 1, 2, 6, 7, 10 | Complete a low-risk task and ask for a revision |
| Looking for templates or prompts | Chapters 8, 16, 20 | Find a reusable template and add your own data, constraints, and verification method |
| Want to use Codex, Claude Code, or Gemini CLI | Chapters 4, 8.13, 8.15, 18 | Distinguish Chat from workspace AI, know which tasks belong in each |
| Want to create skills | Complete a Chapter 7 or 8 exercise first, then Chapter 18 and Appendices | Build a skill from an already-running workflow, not from imagination |
| Manager or team lead | Chapters 3, 12, 17, 19, 20 | Establish a low-risk rollout rhythm, shared templates, and human approval checkpoints |

### 0.4 Seven-day practice schedule

| Day | Goal | Chapters |
| --- | --- | --- |
| 1 | Complete your first low-risk task | 2 |
| 2 | Turn the first version into a second version | 6, 10, 11 |
| 3 | Summarize a customer or user message into an internal brief | 7.2, 8.2 |
| 4 | Check a draft external reply for risks | 7.3, 15 |
| 5 | Pick one scenario from Chapter 8 and run it | 8 |
| 6 | Save a useful assignment method as a template | 16, 19 |
| 7 | Decide whether the workflow is ready to become a skill | 18 |

### 0.5 The core idea in one paragraph

You do not need to memorize many prompts. What actually matters is:
- How to describe work clearly
- How to give AI enough context
- How to stop AI from guessing
- How to verify AI output
- How to save what works for next time

The question to ask before any task is not "Can I do this?" but "Can I let AI run a first draft of this?"

---

## 1. What an AI Work Assistant Is, and Is Not

**What you will learn:** Distinguish between what AI can assist with and what you must decide. Treat every first draft as a draft, not a final answer.

### 1.1 Three principles for building an AI work assistant

**Principle 1: Start with low-risk work.** Do not hand AI tasks involving refunds, pricing, formal customer responses, contracts, or personal data in your first attempts. Start with meeting notes, internal summaries, report drafts, document checks.

**Principle 2: Every first draft is a draft.** AI's first output is not the answer - it is a reviewable, editable starting point. You are responsible for checking what it missed, guessed, or overstated.

**Principle 3: Save useful methods, not just results.** If an assignment saved you time, save three things: how you assigned the task, where AI went wrong, and how you verified the output. That is what becomes a template or skill later.

### 1.2 What AI can assist with

- Organizing scattered content into clear structure
- Producing first drafts of documents
- Checking for logic gaps, tone issues, missing items
- Comparing options
- Breaking down tasks and prioritizing
- Turning recurring processes into SOPs
- Translating complex content into plain language

### 1.3 What AI must not decide for you

AI must not replace your judgment on:
- Final decisions
- External commitments
- Refunds, pricing, or financial transactions
- HR, legal, or contract matters
- Passwords, credentials, or access permissions
- Deleting, sending, publishing, or modifying official data

One sentence to remember:
> AI prepares materials. You make decisions.

---

## 2. Your First Low-Risk Assignment

**What you will learn:** Complete a first low-risk AI task. Write a prompt with goal, data, constraints, and output format. Review the first draft and ask for a revision.

### 2.1 Choose a low-risk task

Suitable first tasks:
- Organize a set of meeting notes
- Turn your scattered notes into action items
- Rewrite an internal paragraph
- Check a document draft for missing items
- Break a requirements description into a list of questions

Not suitable for a first task:
- Replying to a real customer
- Deciding whether to issue a refund
- Modifying official system data
- Analyzing content with full personal data
- Sending announcements, quotes, contracts, or formal emails

### 2.2 Use this assignment format

```
Please help me complete the following task.

Goal:
I want you to help me [describe what you need].

Data:
Here is the content you can reference:
[Paste your meeting notes, message, or text here]

Constraints:
- Do not add information that does not appear in the source material
- If something is uncertain, label it "to be confirmed"
- Do not make final decisions for me
- Do not add commitments or dates that are not in the source

Output format:
Please organize as:
1. Summary
2. Confirmed items
3. Action items
4. Risks
5. Items to confirm
6. Suggested next step
```

### 2.3 Review the first draft - do not accept it immediately

When you receive AI's response, check four things:
- Did it miss anything important that was in the original?
- Did it add information that was not in the original?
- Did it turn "possibly" into "definitely"?
- Are the action items actually actionable?

If you find a problem, do not just say "this is wrong." Specify what is wrong.

### 2.4 Ask for a revision

```
This version needs to be revised.

Problems:
- The second action item has no assigned owner in the original text, but you wrote it as "confirmed"
- The third item does not list what data is still needed

Please rewrite:
- Where there is no confirmed owner, write "to be confirmed"
- Add "what data is needed" to every action item
- Do not add dates that are not in the original
```

### 2.5 Save what worked

If the output was useful, save three things:
1. The type of input (meeting notes, customer message, report summary)
2. How you assigned the task
3. How you verified the output

Do not only save the final answer. What is valuable is "how to assign this type of task next time."

---

## 3. Beginner No-Go Zones

**What you will learn:** Recognize the high-risk tasks beginners most often rush into. Learn to reframe "make a decision" as "help me organize facts and open questions."

### 3.1 Do not make AI the final decision-maker

Instead of:
```
Decide whether this customer should get a refund.
```

Use:
```
Please organize the known facts of this case, the customer's requests, what we have already committed to, what still needs to be confirmed, and what requires a manager's judgment. Do not decide whether to refund.
```

### 3.2 Do not let AI send messages directly

Instead of:
```
Reply to this customer and send it.
```

Use:
```
Please draft a customer reply and list anything that may be risky, requires manager confirmation, or should not be committed to. Do not send it.
```

### 3.3 Do not paste sensitive data

In your first exercises, do not paste:
- Full customer names, phone numbers, or addresses
- Passwords, verification codes, API keys, or tokens
- Full credit card or bank account numbers
- Unpublished contracts, financial data, or HR data
- Unreleased company strategy or pricing

If you need AI to help organize something, de-identify it first:
```
Customer A, a scheduled service on [date], reported a delay and is requesting a refund.
```

### 3.4 Do not treat AI output as company policy

AI may generate plausible-sounding rules that do not exist in your organization. If AI writes:

```
Most companies complete refunds within three business days.
```

And your company has no such rule, that sentence cannot be used. Ask AI to label it instead:
```
Company policy not provided. Needs confirmation from manager or finance.
```

---

## 4. Tools, Chat, Workspace AI, CLI Agents, and Skills

**What you will learn:** Distinguish between tools, usage approaches, and skills. Know when a general Chat interface is enough and when a workspace agent like Codex, Claude Code, or Gemini CLI is appropriate.

### 4.1 Chat versus delegation

Chatting is: ask a question, get an answer.

Delegation is: give AI a goal, data, constraints, and a verification standard, and get a work product you can continue to refine.

Most problems with AI output are not tool problems - they are delegation problems.

### 4.2 You probably need fewer tools than you think

Many tasks that seem to need a specialized tool can be handled by mainstream AI like ChatGPT, Claude, or Gemini - if you delegate clearly.

| What you want to do | Instead of finding a new tool, try this first |
| --- | --- |
| Organize meeting notes | Ask AI to separate decisions, action items, owners, deadlines, risks, and open questions |
| Check a report for anomalies | Ask AI to find anomalies, list possible causes, and note what data is still needed |
| Draft a customer reply | Ask AI to preserve the original meaning, add no new commitments, and flag risks |
| Organize a requirements document | Ask AI to separate goals, scope, undefined questions, and risks |

If your assignment is "help me organize this," switching tools will not fix the result. A clear assignment on a mainstream tool almost always outperforms a vague assignment on a specialized one.

### 4.3 When you actually need a new tool

| Situation | Verdict | Next step |
| --- | --- | --- |
| Only summarizing, rewriting, classifying, checking | Usually no new tool needed | Practice delegating on mainstream AI |
| Need to connect to company systems, email, calendar, project tools | May need a connector or authorized tool | Confirm permissions and data scope first |
| Need large-scale batch processing with fixed formats | May need templates or automation | Run a human-verified version first |
| Need to send, delete, or modify live data | High risk | Require human approval before automation |
| Mainstream AI tried and consistently fails | Possible data, process, or tool limit | Diagnose the failure before evaluating new tools |

### 4.4 Chat versus workspace and CLI agents

| Dimension | General Chat | Workspace / CLI Agent |
| --- | --- | --- |
| Examples | ChatGPT, Claude, Gemini chat interfaces | Codex, Claude Code, Gemini CLI |
| Best for | Questions, rewrites, summaries, brainstorming, draft generation | Reading multiple files, editing documents, running commands, organizing folders |
| Primary output | A text response | Actual files, diffs, check results, deliverables |
| Context source | What you paste into the conversation | Conversation plus workspace files and project rules |
| Key risk | May guess or overstate | May actually edit files or run commands |
| What matters most | Clear question, requested format, verified answer | Defined scope, read-before-write, confirm before modify, review changes |

### 4.5 Which to use

Use Chat for:
- Asking a concept question
- Rewriting a paragraph
- Summarizing a small piece of content
- Generating prompt or skill drafts
- Checking pasted content

Use Codex, Claude Code, or Gemini CLI for:
- Reading an entire folder or multiple files
- Modifying Markdown, documents, code, or config files
- Running tests, checking formatting, or executing commands
- Organizing a repo or local folder
- Writing a skill as an actual file
- Producing output that lives in your workspace, not just in a chat window

### 4.6 First-time safety assignment for workspace agents

Because workspace agents can actually read, edit, and run things, start with read-only:

```
Please do not modify any files yet.

Please read the relevant documents in this folder and understand the current content and structure.

Goal: I want to accomplish [describe the goal].

Please report back:
1. Which files you read
2. The main thread of the current content
3. What you think needs to change
4. Which files you recommend modifying
5. What you need me to confirm

Wait for my confirmation before starting to modify anything.
```

Workspace agents are more capable, which means you need to be more precise about scope, boundaries, and verification.

---

## 5. Choosing the Right Tasks

**What you will learn:** Identify which tasks are suitable for AI and which are not. Recognize six categories of work that fit the AI-first-draft approach.

### 5.1 Task categories that work well

**Organizing:** Meeting notes, customer messages, emails, survey responses, interview notes, scattered notes.
**Rewriting:** Customer replies, internal announcements, event copy, SOP language, presentation scripts.
**Checking:** Document drafts, customer replies, reports, SOPs, FAQs, external announcements.
**Comparing:** Options, tools, vendors, processes, plans.
**Decomposing:** Projects, events, complex tasks, cross-team workflows.
**SOP drafting:** Recurring processes, customer service flows, form reviews, report organizing, application review.

### 5.2 Tasks that require human judgment - AI can help organize, not decide

- Whether to issue a refund
- Whether to submit a quote
- Whether to make a commitment to a customer
- Whether to delete data
- Whether to change permissions
- Whether to send a formal email
- Whether to publish an announcement
- Whether to sign a contract
- Whether to process sensitive personal data

The pattern is: ask AI to organize the facts, options, and open questions - then you decide.

---

## 6. The Assignment Formula

**What you will learn:** Use four elements - goal, data, constraints, verification - to write a clear assignment. Turn vague requests into actionable tasks.

### 6.1 Four elements of a clear assignment

**1. Goal** - What do you want AI to complete?
```
Help me organize this meeting recording into a list of action items.
```

**2. Data** - What can AI reference?
```
Below are today's meeting notes including the discussion content and decisions made.
```

**3. Constraints** - What must AI not do?
```
Do not add information not mentioned in the notes; label anything uncertain as "to be confirmed."
```

**4. Verification standard** - What should the output look like?
```
Please output as: decisions, action items, owners, deadlines, risks, open questions.
```

### 6.2 Universal assignment template

```
Please help me complete the following task.

Goal:
I want you to help me [describe what you need].

Data:
Here is the content you can reference:
[Paste content here]

Constraints:
- Do not add information not in the source material
- Label anything uncertain as "to be confirmed"
- Do not make final decisions for me
- Do not add commitments that are not in the source

Output format:
Please organize as:
1. Summary
2. Confirmed items
3. Action items
4. Risks
5. Open questions
6. Suggested next step
```

---

## 7. Practice Loops

**What you will learn:** Build hands-on practice with three exercises covering meeting notes, customer message triage, and external reply checking.

This chapter is not for reading - it is for doing. Complete the three exercises in order.

### 7.1 Exercise 1: Meeting notes into action items

**Goal:** Turn scattered content into a trackable work list.

**Scenario:** After a planning meeting, you have notes about a website, a participant list, an FAQ, and several undecided items. Asking AI to "summarize this" gives you a summary that looks clean but cannot actually be tracked.

**Better assignment:**
```
Please organize the following meeting notes into an internal tracking summary.

Goal: I need to know what has been discussed, what needs to be done next, and what is still undecided.

Data: [Paste meeting notes]

Constraints:
- Do not add information not mentioned in the notes
- Write "unassigned" where there is no confirmed owner
- Write "not specified" where there is no confirmed date
- Do not decide budget or channel questions yourself

Output:
1. Meeting highlights
2. Known action items
3. Likely responsible roles
4. Known deadlines
5. Items to confirm
6. First suggested next step
```

**What to verify:** Did AI miss any undecided items? Did it write unconfirmed owners as confirmed? Did it add dates that were not in the original?

**Common error and how to fix it:**
If AI writes "Marketing will complete copy by Wednesday," but the original only said "design needs copy by Wednesday noon," it has overstated the commitment. Correct it specifically:
```
Please change "Marketing will complete copy by Wednesday" to "Design needs copy by Wednesday noon; copy owner and completion time to be confirmed."
```

### 7.2 Exercise 2: Customer message into internal brief

**Goal:** Organize a case before responding - never let AI reply to a customer without a human decision.

**Assignment:**
```
Please organize the following customer message into an internal handling brief.

Goal: Do not reply to the customer yet. I need to know the customer's request, confirmed facts, inferences, risks, and what to check before responding.

Data: [Paste customer message]

Constraints:
- Do not commit to a refund or compensation
- Do not admit company liability
- Do not treat the customer's mention of other people's experience as confirmed fact
- Do not use language that could escalate the customer's frustration

Output:
1. Customer's main request
2. Customer's tone and emotional risk
3. Confirmed information
4. Reasonable inferences
5. Items still to confirm
6. Items we cannot commit to directly
7. Suggested internal next step
```

### 7.3 Exercise 3: Check an external reply draft for risk

**Goal:** Use AI as a checker, not just a writer.

**Assignment:**
```
Please check the following external reply draft for risks.

Goal: List only the problems and suggested changes. Do not rewrite the entire message.

Data: [Paste the draft]

Please check for:
1. Improper commitments
2. Admission of liability
3. Unconfirmed facts stated as facts
4. Overguarantees
5. Anything that needs manager confirmation

Constraints:
- Do not add company policy that was not provided
- Do not decide whether to refund
- Do not assume the company has confirmed liability
```

**After completing all three exercises you should be able to:**
- Turn vague requests into specific assignments
- Distinguish facts from inferences from open questions
- Spot when AI has made a commitment it should not have
- Request a specific revision instead of just saying "redo this"

---

## 8. Everyday Workflow Scenarios

**What you will learn:** Apply the assignment method to different work situations. Learn to choose between Chat, workspace AI, and Computer Use based on task type.

### 8.1 Choosing your first scenario

Pick a scenario you encounter at least once per week, with data that is not sensitive and output you can verify yourself.

| Priority | Good first scenario | Why |
| --- | --- | --- |
| 1 | Meeting notes, internal notes, action items | Low risk, easy to spot errors |
| 2 | Internal document rewrites, SOP drafts | Easy to revise, easy to save as template |
| 3 | Report summaries, event results | Practice separating facts from inferences |
| 4 | Customer message summaries | Risk-labeling practice - do not let AI reply directly |
| 5 | Expense reports, application reviews | Needs clearer safety boundaries |
| 6 | Admin console manual, storage cleanup | Workspace or Computer Use, confirm permissions first |

Before picking a scenario, ask yourself:
- If this goes wrong, does it immediately affect customers, money, contracts, or official data?
- Do I have enough background knowledge to verify AI's first draft?
- Will this come up again? Is it worth saving as a template?

### 8.2 Short scenario templates

**Meeting notes:** Ask AI to separate decisions, action items, owners, deadlines, risks, and open questions. Label missing information as "not specified."

**Customer message:** Ask AI to organize the customer's main concern, current tone, confirmed facts, what we have already committed to, what we cannot commit to, and the suggested next step. Do not let AI write the reply directly.

**Report anomaly check:** Ask AI to find anomalies, list possible causes (labeling them as inferences), note what data still needs to be checked, and suggest a priority order. Do not let AI turn inferences into conclusions.

**SOP draft:** Ask AI to include applicable situations, preparation steps, operating steps, notes, common errors, completion checks, and when to escalate to a manager.

### 8.3 Advanced case: Using a workspace agent to create an admin console operation manual

Many admin panels, member systems, order systems, or internal tools have many pages and buttons that need to be organized into a manual team members can use. Doing this manually means opening pages one by one, taking screenshots, masking sensitive data, writing steps, and formatting everything.

This kind of work is well-suited for AI because it involves large amounts of page observation, screenshot labeling, description, and formatting - but still requires a human to control login, permissions, and scope.

**What the human handles first:**
1. Log in to the admin system yourself
2. Prefer a test, demo, staging, or read-only account
3. Open the system to the starting page you want AI to observe
4. Decide which sidebar pages, tabs, and sections AI can navigate
5. Avoid pages you should not expose: payment, personal data, permissions, system settings
6. Explicitly limit AI to observe, navigate, screenshot, and organize - no modifications

**Assignment:**
```
Please help me create the first draft of an operation manual for this admin console using Computer Use.

Goal: Produce a manual team members can follow, covering main pages, functions, buttons, fields, and basic operating steps.

Data: I am already logged in and have opened the system to the starting page you can view. If this is not a test, demo, staging, or read-only account, please remind me to confirm the permission risk first.

You may:
- Observe menus, buttons, fields, and labels on the current page
- Click sidebar items, tabs, and expandable menus that only switch the view
- Survey the main features and page structure
- Capture screenshots within the safe scope and organize operating steps
- Produce a Markdown operation manual draft

You must not:
- Log in or ask for passwords
- Click add, edit, delete, save, submit, publish, modify settings, pay, or change permissions
- If unsure whether a button modifies data, stop and ask me
- Download or share sensitive data
- Guess the purpose of unclear functions
- Screenshot pages containing customer names, phone numbers, transactions, payments, or credentials without first alerting me to mask them

Output:
1. Feature overview
2. Sidebar page list
3. Purpose of each page
4. Main fields and buttons per page
5. Basic operating steps
6. Screenshot recommendations
7. Open questions
8. Items AI should not judge or operate
```

**What the human must verify:**
- Did AI miss any sidebar pages?
- Does each step match the actual screen?
- Are screenshots masked for sensitive data?
- Did AI stay within observe-and-navigate only?
- Are unclear functions labeled as "to be confirmed"?
- Can a team member actually follow this manual?

### 8.4 Safety cleanup case: disk space and unknown software risk

When a computer runs out of storage, many people's first response is to search for "free cleanup software." This is risky.

Some cleanup tools that appear legitimate may ask you to download a `.dmg` file, install a profile, enter your system password, grant full disk access, and then read your browser, email, cloud files, or saved credentials. The worst outcome is not a messy disk - it is having your account sessions, cloud data, or work system permissions compromised.

When you run low on storage, do not look for cleanup software first. A better approach: within the tools and environment your organization permits, ask a workspace agent like Codex, Claude Code, or Gemini CLI to use built-in system commands to conduct a read-only survey first. Let AI identify what is using space, categorize candidates for cleanup, and flag what must not be touched. Do not install unknown cleanup tools, and do not run scripts you do not understand.

**What a workspace agent can do:**
- Survey current disk usage
- Identify the largest folders
- Distinguish commonly used, likely unused, and clearly temporary files
- Produce a cleanup candidate list with risk labels
- Flag folders and file types that must not be touched

**What AI must not do:**
- Download or install any external cleanup software
- Delete files without a confirmed list
- Touch browser data, email, credentials, cloud-synced folders, or work project files
- Use permanent deletion commands
- Treat "not modified recently" as equivalent to "safe to delete"

**Assignment:**
```
Please help me do a safe cleanup of low disk space.

Constraints:
- Do not delete any files yet
- Do not download or install any cleanup software
- Do not touch passwords, browser data, email, cloud-synced folders, work projects, or system settings
- Do not use permanent deletion
- Start with a read-only survey

Please report:
1. Current disk space remaining
2. Largest folders or file types
3. Low-risk candidates you think can be cleaned up
4. Candidates that need my confirmation before touching
5. High-risk folders or file types that must not be touched
6. Estimated maximum space that could be freed

Please output as a table with: path, size, type, likely use, frequency (frequent/infrequent/unknown), suggested action, deletion risk, whether my confirmation is needed.
```

**What this scenario is really teaching:**
> Do not download unknown cleanup software to solve a storage problem. Use a workspace AI agent to do a safe read-only survey first, then decide yourself what to remove.

AI's role here is not to delete things - it is to help you understand where space is going, categorize cleanup candidates by risk, and avoid high-risk data. The person who clicks confirm is always you.

---

## 9. Diagnosing Bad Assignments

**What you will learn:** Understand why vague or risky assignments produce inconsistent results. Practice rewriting problem assignments.

### 9.1 Too short, too vague

```
Help me organize this.
```

Problems: AI does not know who this is for, how detailed it should be, what format to use, whether it can make inferences.

### 9.2 Good structure: goal, format, constraints

```
Please organize the following customer conversation into an internal handling summary.

Purpose: Let the customer service manager quickly understand the current status of this case.

Output:
1. Customer's request
2. Background
3. What we have committed to
4. What is still unconfirmed
5. Possible risks
6. Suggested next step

Constraints:
- Do not add information not in the conversation
- Do not decide whether to refund
- Label anything uncertain as "to be confirmed"
```

### 9.3 Letting AI decide high-risk items

```
This customer is angry. Tell him we can give a refund.
```

Problems: Refund decisions belong to a manager or finance team. AI cannot commit on behalf of the company. This may create follow-up disputes.

Better:
```
This customer is upset. Please help me organize:
1. Why the customer is upset
2. What the customer is asking for
3. What we have previously committed to
4. Whether there is any refund-related information
5. Questions we need manager confirmation on

Do not write a formal reply yet.
```

---

## 10. Verification: Do Not Accept Output Blindly

**What you will learn:** Apply four verification questions to every AI output. Build the habit of reviewing before accepting.

### 10.1 Four verification questions

Every time you receive AI output, ask:

1. **Did it miss anything?** Is important information from the source missing?
2. **Did it guess?** Did it turn "possibly" into "certainly"?
3. **Did it overstate?** Did it commit to something it should not have?
4. **Can it be handed off?** Can the next person read this and take action?

### 10.2 Common errors

**Error 1: Inference stated as fact**
AI writes: "The customer is likely dissatisfied because of the price."
If the original did not mention price, this is a guess.
Correct version: "Reason for dissatisfaction not clearly stated; may relate to price but needs confirmation."

**Error 2: Added information**
AI writes: "We will complete the process within three business days."
If your company has not committed to this timeframe, it cannot be in the output.
Correct version: "We will confirm the case status and reply with the next steps as soon as possible."

**Error 3: Advertising tone**
AI writes: "We deeply value your precious feedback and will strive to provide the most outstanding service."
Replace with: "We have received your feedback and will confirm the situation, then reply with the available next steps."

**Error 4: Output looks complete but cannot be executed**
AI writes: "We recommend improving internal processes, strengthening communication, and increasing efficiency."
This is too abstract. No owner, no next step, no standard.
Ask AI to revise: "Please rewrite each recommendation as a concrete action item with: what to do, who is responsible, what data is needed, and how to know it is done."

---

## 11. Refinement: Make the Second Version Useful

**What you will learn:** Give AI specific, targeted feedback instead of just saying "redo this." Use the refinement formula to produce a more useful second version.

### 11.1 Do not just say "rewrite"

Poor feedback:
```
Wrong. Rewrite.
```

AI does not know what was wrong and will likely produce another version with the same problems.

Better feedback:
```
This version has problems:
1. The tone sounds like advertising copy
2. It added a commitment that was not in the original
3. It did not list the open questions

Please rewrite it as an internal customer service summary. Keep the customer's original request. Do not add a handling timeline.
```

### 11.2 Refinement formula

```
This version needs revision.

Problems:
- [Problem 1]
- [Problem 2]

Reason:
- [Why this is a problem]

Please revise to:
- [What you want instead]

Must keep:
- [What should stay]

Must not include:
- [What should be removed]
```

---

## 12. Safety Boundaries

**What you will learn:** Know which data and actions should never be handed to AI. Practice de-identifying sensitive data. Understand when to require human confirmation.

### 12.1 Data that should not be pasted into AI without authorization

Unless your organization has a clear authorization and secure environment:
- Passwords or API keys
- ID numbers
- Credit card or bank account data
- Full customer personal records
- Unpublished financial data or contracts
- Internal confidential strategies

### 12.2 How to handle sensitive data

De-identify first.

Original:
```
John Smith, phone 0912-xxx-xxx, order #A12345, requesting a refund.
```

Revised:
```
Customer A, one order, requesting a refund.
```

Then assign:
```
The following data has been de-identified. Please help organize the case background, customer requests, confirmed information, and open questions. Do not attempt to identify the customer.
```

### 12.3 External content always requires human confirmation before sending

AI can draft any of the following, but a human must confirm before sending:
- Formal customer replies
- External announcements
- Social media posts
- Contract terms
- Quotes
- Apology statements
- Recruitment or HR notices
- Financial-related communications

---

## 13. Assignment Quality Levels

**What you will learn:** Use a five-level scale to assess your assignments. Know how goal, format, constraints, and verification standards each improve output stability.

### Level 1: One-line assignment

```
Help me organize this.
```

Problem: Too vague. AI does not know the purpose or format.

### Level 2: Has a goal

```
Help me organize this into a summary for my manager.
```

Better than Level 1, but no format guidance.

### Level 3: Has a format

```
Help me organize this into a summary for my manager, divided into background, current status, risks, and next steps.
```

Can produce a usable first draft.

### Level 4: Has constraints

```
Help me organize this into a summary for my manager, divided into background, current status, risks, and next steps. Do not add information not in the source; label anything uncertain as "to be confirmed."
```

Reduces guessing and fabrication.

### Level 5: Has a verification standard

```
Help me organize this into a summary for my manager, divided into background, current status, risks, and next steps. Do not add information not in the source; label anything uncertain as "to be confirmed." Every next step must include a responsible role, what data is needed, and a completion standard.
```

Closest to a handoff-ready, verifiable assignment.

---

## 14. Confidence Labels

**What you will learn:** Ask AI to distinguish confirmed information, reasonable inferences, and items still to be confirmed. Reduce the risk of AI presenting guesses as facts.

### 14.1 Basic template

```
Please divide the output into:
1. Confirmed information
2. Reasonable inferences
3. Insufficient data - needs human confirmation
```

### 14.2 When to use it

Especially useful for:
- Customer complaint summaries
- Report anomalies
- Manager decision briefs
- External reply drafts
- Expense reimbursement checks
- Any case where input data is incomplete

### 14.3 Example output

```
Confirmed information:
- Customer emailed on May 1 saying the product was not received.
- Order status currently shows "shipped."

Reasonable inferences:
- Possibly a logistics delay or wrong delivery address, but not yet confirmed.

Insufficient data - needs human confirmation:
- Logistics delivery record
- Whether the delivery address is correct
- Whether there is an existing customer service reply
```

---

## 15. Pre-Send Checklist for External Replies

**What you will learn:** Build a risk check routine before sending any external content. Learn to use AI as a checker, not a sender.

Before sending any external content, verify:

- No commitment to price, refund, compensation, discount, or handling timeline
- No admission of company liability
- No exposure of internal processes
- No mention of inappropriate names, customer data, or internal information
- Stable, non-escalating tone
- No inference presented as confirmed fact
- Confirmed whether manager, finance, legal, or PR needs to review
- Consistent with existing company rules
- Leaves room for follow-up confirmation

Ask AI to help check before sending:

```
Please check this external reply draft for the following risks:
1. Improper commitments
2. Admission of liability
3. Leaked internal information
4. Escalating language
5. Inference presented as fact
6. Items that need manager confirmation but are not labeled

Please only list the problems and suggested changes. Do not rewrite the entire message.
```

---

## 16. Template Library

**What you will learn:** Get copy-ready templates for common tasks. Know that templates must always be adapted, not used as-is.

Every template below needs you to add your specific goal, data, and constraints before using.

**Meeting notes to action items:**
Ask AI to output: decisions, action items, owners, deadlines, risks, open questions. Label missing information as "not specified."

**Customer message to internal summary:**
Ask AI to output: customer request, customer tone, confirmed facts, what we have committed to, what we cannot commit to, suggested next step, open questions.

**Customer reply polishing:**
Ask AI to rewrite as clear, polite, non-confrontational, and non-overcommitting. Keep the original meaning. No new commitments. No internal process details.

**Document draft logic check:**
Ask AI to find: logic contradictions, missing information, inappropriate tone, easily misunderstood sections, suggested revision directions.

**SOP draft:**
Ask AI to include: applicable situations, preparation steps, operating steps, notes per step, common errors, completion checks, when to escalate.

**Report anomaly summary:**
Ask AI to separate: confirmed anomalies, possible causes (labeled as inferences), data still needed for verification, priority recommendation. Do not let it turn inferences into conclusions.

**Manager decision brief:**
Ask AI to output: background, current status, available options, risks of each option, recommended option, what the manager needs to decide.

---

## 17. Red-Flag Rules

**What you will learn:** Know when to stop and ask a human. Distinguish data gaps, high-risk decisions, formal operations, and permission issues.

Stop and ask a human when:

- Data is insufficient but a decision is required
- The task involves money, refunds, contracts, or personal data
- An external commitment is about to be made
- A customer threatens a complaint, lawsuit, or public disclosure
- You cannot understand what AI produced
- The same problem persists through three revision attempts
- The output affects other departments
- The action involves deleting, overwriting, publishing, or changing permissions
- The task requires formal legal, tax, HR, or financial judgment

Stopping is not failure - it is risk control.

---

## 18. Turning Reusable Workflows into Skills

**What you will learn:** Understand that a skill is a saved, verified workflow - not just a polished prompt. Learn the five-step path from collaboration to skill packaging. Know when a template is enough and when a formal skill is worth it.

### 18.1 What is a skill

A skill is a set of standing instructions written for AI. Not a single prompt, but a complete workflow that has been run, corrected, and verified - then saved for reuse.

Think of it as: "The standard operating procedure I wrote for my AI work assistant."

### 18.2 When is a workflow worth turning into a skill

A workflow is worth packaging as a skill when it:
- Happens every week
- Is done by multiple people
- Requires re-explaining the rules every time
- Has frequent errors
- Has consistent input types
- Has consistent output format
- Has a clear verification method

### 18.3 A good skill includes

| Field | Purpose |
| --- | --- |
| Skill name | What work does this handle |
| Applicable situations | When to use it, when not to |
| Required data | What to prepare before running |
| Operating steps | What AI should do in what order |
| Output format | What the final output looks like |
| Verification method | How the human checks whether it is usable |
| Common errors | What AI typically misses, guesses, or overstates |
| Stop conditions | When to pause and ask a human |
| Helper files | Advanced skills may include `.sh` or `.py` scripts |

### 18.4 A workflow usually cannot become a skill in one step

Do not start by asking AI to "create a skill for me." Complex workflows have multiple phases, different types of data, various roles involved, and edge cases that are not obvious until you have run the process several times.

A rushed one-shot skill looks complete but is built on guesses. The reliable path is:

| Step | What to do | Why |
| --- | --- | --- |
| First: collaborate | Run the actual work step by step | AI learns the real process, not an imagined one |
| Second: verify each phase | Check errors and add constraints as you go | Discover where AI tends to guess or misjudge |
| Third: debrief | Ask AI to summarize what worked and where human judgment was needed | Turn the interaction into a discussable process |
| Fourth: evaluate | Assess whether this is ready to be a skill | Avoid packaging an immature process |
| Fifth: package | Only then write it as a template or skill draft | Built on verified behavior |

Start a large workflow like this:
```
This is a larger workflow. Please do not rush to create a skill.

Please help me work through this step by step.
After each phase, report:
1. What you did
2. What data you used to decide
3. What you were uncertain about
4. What needs my verification
5. What you recommend for the next phase

After we finish the whole task, we can review whether it makes sense to package this as a template or skill.
```

### 18.5 Skills and helper scripts

A beginner skill can be a single `SKILL.md` file. A more mature skill may be a small folder:

```
my-skill/
  SKILL.md
  scripts/
    check-input.sh
    parse-report.py
  templates/
    output-template.md
  examples/
    sample-input.csv
    sample-output.md
```

Helper scripts are different from text instructions - they actually read files, modify files, delete files, connect to the network, or execute commands. Any skill with `.sh` or `.py` files requires an extra layer of scrutiny:

- Which folders will the script read?
- Will it modify or delete files?
- Will it connect to the network or download anything?
- Will it read passwords, tokens, API keys, browser data, or personal data?
- Does it require a system password or elevated permissions?
- If it fails mid-run, does it leave broken files or corrupt the original data?
- Is there a dry-run or read-only mode?

**Beginner rule:**
> You can ask AI to generate a script draft, but do not run scripts you do not understand. Ask AI to explain every section: what it does, which files it touches, what the risks are - then decide whether to run it.

### 18.6 Skill draft template

```
# Skill Name

[Name here]

## Purpose

This skill helps [describe use case].
Its goal is not [what it does not do], but [what it does do].

## Applicable Situations

Use when [description].

Suitable for:
- [situation]
- [situation]

Not suitable for:
- [situation]
- [situation]

## Required Data

The user should provide:
- [item]
- [item]
- [item]

If data is missing, list what is missing and do not guess.

## Operating Steps

1. Confirm the task goal and data scope
2. Organize confirmed information
3. Label reasonable inferences
4. List items to be confirmed
5. Output in the specified format
6. Check whether any stop conditions apply

## Output Format

Please output:
1. [item]
2. [item]
3. [item]

## Safety Constraints

AI must not:
- [action]
- [action]

## Stop Conditions

If any of the following occur, stop and alert the user:
- [condition]
- [condition]

## Verification Method

The user should check:
- [check]
- [check]

## Common Errors

AI frequently makes these mistakes:
- [error]
- [error]

Correction: [how to fix]

## Helper Files (Advanced)

Does this skill need `.sh`, `.py`, templates, or example files?
If not: keep only `SKILL.md`.
If yes: describe each file's purpose, what it reads, what it modifies, what it must not touch, whether it supports dry-run, and what needs human confirmation before running.
```

### 18.7 The skill progression ladder

One-time prompt -> Personal template -> Team template -> Skill

Master stable delegation before thinking about skill packaging.

---

## 19. Team Adoption and Knowledge Capture

**What you will learn:** Turn individual AI experience into team-shareable templates and processes. Build a sustainable rhythm for small-team adoption.

### 19.1 Individual adoption: start with one small task

Each team member should pick one task that:
- Happens at least once a week
- Normally takes 15+ minutes to organize
- Does not involve formal commitments or high-risk decisions
- Can be easily verified if AI makes an error
- Produces output the next person can act on

### 19.2 Team adoption: collect one good case per week

Use a simple format:

```
Case name:
Original task: How was this done before? How long did it take?
Assignment method: How did you ask AI to do it?
AI output: What did AI produce?
Human verification: What did you check? Where did AI make errors?
Improvement or time saved:
What to change next time:
```

Do not only collect success stories. Failed or incorrect cases have more teaching value because they become verification rules.

### 19.3 When a prompt is ready to become a team template

A prompt is ready to become a team template when:
- At least two people have used it
- It has been run at least three times
- Input type is consistent
- Output format is consistent
- There are clear items AI must not do
- There is a clear verification method

### 19.4 When a team template is ready to become a skill

When a team template is stable enough that:
- Applicable situations are clear
- Input data is predictable
- Operating steps are fixed
- Risk boundaries are clear
- Stop conditions are clear
- Different users consistently produce stable results

Do not rush skill packaging. Premature skills institutionalize unverified processes.

### 19.5 Where to store knowledge

| Type | Content | Best for |
| --- | --- | --- |
| Personal note | Your own useful assignment methods | Prompts still being tested |
| Team template | Reusable formats multiple people use | Meeting summaries, customer message briefs, expense checks |
| Skill or SOP | Verified, mature workflows | High-risk customer triage, expense reimbursement, email attachment review |

Do not store: full customer personal data, passwords or credentials, unpublished contracts or financial data, sensitive complete conversations.

### 19.6 How managers can drive adoption

1. Each person picks one low-risk task to try
2. Share one success or failure case per week
3. Collect recurring good prompts into team templates
4. Add human approval checkpoints for high-risk tasks
5. After one month, evaluate which workflows are ready for skill packaging

The question to measure is not "how often did people use AI." The right questions are:
- Does it save organizing time?
- Does it reduce missed items?
- Does it make handoffs cleaner?
- Does it lower the risk of accidental commitments?
- Does it produce reusable templates?

---

## 20. One-Page Quick Reference

### Before assigning

Ask yourself:
- What do I want AI to complete?
- What data can I give it?
- What must it not do?
- What format should the output be in?
- How will I know if it is usable?

### When reviewing output

Check:
- Did it miss anything?
- Did it guess something?
- Did it overstate anything?
- Does it violate any company rules?
- Did it expose any sensitive information?
- Can the next person act on this?

### Universal quick template

```
Please help me handle the following.

Goal:
[What you need]

Data:
[Paste content]

Constraints:
- Do not add information not in the source
- Label anything uncertain as "to be confirmed"
- Do not make final decisions for me
- Do not add commitments not in the source

Output:
1. Summary
2. Confirmed items
3. Items to confirm
4. Risks
5. Suggested next step
```

### High-risk task quick check

When the task involves: refunds, compensation, quotes, discounts, contracts, legal, tax, HR, external announcements, formal emails, customer commitments, deletion, overwriting, publishing, changing permissions, personal data, money, or confidential information:

AI can only help organize or draft. Use this safe assignment phrase:
```
Please organize the facts, inferences, open questions, and risks. Do not make final decisions for me and do not add commitments.
```

### Key principles

- Chatting asks for an answer. Delegation starts work.
- AI's first version is a draft, not a final answer.
- AI can speed you up, but you guard the boundaries.
- You do not need many AI tools. Go deeper on a few mainstream ones.
- Often the problem is not that the tool cannot do it - it is that you have not learned how to delegate it.
- Do not fear AI entering your work. Fear delegating your judgment along with your tasks.
- A skill is not a stored prompt. It is a saved, verified, repeatable workflow.
- One person using AI well speeds themselves up. A team sharing templates and skills speeds the organization up.

### Chat / workspace agent / skill decision table

| What you are doing now | Recommended approach |
| --- | --- |
| Asking a concept, rewriting a short text | General Chat |
| Summarizing a small piece of pasted content | General Chat |
| Generating a prompt or skill draft | General Chat or workspace agent |
| Reading multiple files, documents, or folders | Codex / Claude Code / Gemini CLI |
| Modifying files, organizing folders, running checks | Codex / Claude Code / Gemini CLI |
| Writing a verified workflow as a formal SKILL.md | Workspace agent or manual |
| Something multiple people use with consistent format | Template first, then skill when stable |
| Anything involving deletion, sending, publishing, changing permissions, money, or personal data | Stop and confirm with a human first |

---

## 21. Closing

AI does not give a perfect answer the first time.

A more realistic expectation is:
1. AI produces a first draft
2. You find the problems
3. You specify what needs to change
4. AI produces a second draft
5. You save the useful method for next time

Using AI well is not about memorizing commands.

What actually matters:
- Knowing what to delegate
- Knowing what not to delegate
- Seeing where AI went wrong
- Explaining clearly how to revise it
- Turning good methods into reusable workflows

Start with low-risk, small-scale work. When you can consistently complete the assign-verify-refine cycle, an AI work assistant stops being a chat tool and starts being a genuine work partner.

The goal of learning AI is not to make yourself an appendage of the tool. It is to make your own work judgment clearer. The person who can direct AI to produce verifiable, deliverable, continuously improving output is not just a user - they are a trainer, a verifier, and a process designer. That kind of person does not just complete tasks faster; they build methods that other people can use.

---

## Appendix A: Skill Example - High-Risk Customer Message Triage

> This skill is not for labeling customers. It helps customer-facing staff organize facts, reduce the risk of accidental commitments, and determine whether a case needs escalation - especially in high-emotion, high-pressure situations.

### A.1 Skill Name

`High-Risk Customer Message Triage`

### A.2 Applicable Situations

Use when a customer service interaction involves:
- Strong customer emotion or repeated accusations
- Requests for refunds, compensation, discounts, or exceptions
- Threats to complain, post negative reviews, or take legal action
- Repeated topic-jumping or demands exceeding policy
- Denial of previous conversation records
- Demands for immediate commitments
- Threatening or coercive language
- Risk of escalation to PR, legal, or management

### A.3 Required Data

1. Customer's original message (preserve the exact words, not just an impression)
2. Case background (order, service, event, contract, payment status, timeline)
3. Previous replies (what customer service has already said or committed to)
4. Company rules (refund policy, service terms, compensation standards, permission scope)
5. What customer service wants to achieve (de-escalate, confirm facts, decline an unreasonable request, escalate, document)

### A.4 Assignment Template

```
Please help me triage the following customer case using the high-risk customer message method.

Goal: Do not reply to the customer yet. Please help me assess the case status, risks, response direction, and whether escalation is needed.

Data:
[Customer's original message]
[Case background]
[Previous commitments or replies]
[Company rules or constraints]

Constraints:
- Do not commit to refunds, compensation, discounts, or exceptions on behalf of the company
- Do not use language that demeans the customer
- Do not state inferences as facts
- Do not suggest customer service argue with the customer
- Do not provide legal conclusions
- Label anything uncertain as "to be confirmed"
- If legal, PR, security, personal data, or financial issues are involved, flag as "escalation required"

Output:
1. Case summary
2. Customer's main request
3. Customer tone and communication risk
4. Confirmed facts
5. Unconfirmed items
6. What we have committed to
7. What we cannot commit to
8. Risk level (L1-L4)
9. Recommended handling strategy
10. Suggested reply direction
11. Whether manager / legal / PR escalation is needed
12. Internal case notes
```

### A.5 Risk Levels

**L1 - General dissatisfaction:** Customer is unhappy but still describing the problem. No threats of complaint or legal action. Customer service can respond per standard procedures.

**L2 - High-emotion complaint:** Strong customer emotion. Repeatedly requesting exceptions. Needs more careful tone but still manageable by customer service.

**L3 - Escalation risk:** Customer threatens complaint, negative review, or public disclosure. Involves refund, compensation, personal data, or payment dispute. Manager should confirm before responding.

**L4 - Legal or PR risk:** Customer mentions lawsuit, media, regulatory authority, or public disclosure. Involves major financial disputes, contract issues, or data concerns. Customer service should not respond independently.

### A.6 Safe reply language

Use:
- "We have received your feedback."
- "We will confirm the relevant records first."
- "We need to clarify [specific item] before responding."
- "We will reply with the available next steps after confirming."
- "This part requires confirmation via company procedure. Customer service cannot commit directly."

Avoid:
- "You misunderstood."
- "This is not our problem."
- "Rules are rules."
- "That's impossible."
- "You said that before."
- "We will definitely give you a refund."
- "We guarantee this will be resolved."

### A.7 Stop Conditions

AI should flag "escalation required" and not suggest customer service handle independently when:
- Customer mentions legal counsel, lawsuit, or regulatory body
- Customer threatens media coverage or public disclosure
- Personal data breach is involved
- Large financial amount or compensation is involved
- Contract interpretation is at issue
- Physical threats or harassment
- Customer demands deletion of records
- Customer requests internal company materials
- Customer demands bypassing company procedures
- Customer service has responded multiple times but conflict continues to escalate

### A.8 Verification Checklist

After using this skill, verify:
- Facts and inferences are clearly separated
- Committed and uncommitted items are listed
- No language that could escalate the customer
- No direct commitments to refund, compensation, or discount
- Escalation need has been assessed
- Case timeline and conversation records are preserved
- Draft reply can be reviewed by a manager

---

## Appendix B: Skill Example - Expense Reimbursement Completeness Check

> This skill is not for AI to decide whether an expense can be reimbursed. It helps team members organize data, check for missing items, and complete purpose descriptions before submitting to finance. Finance review and final approval follow company policy.

### B.1 Skill Name

`Expense Reimbursement Completeness Check`

### B.2 Applicable Situations

Use when a team member needs to submit an expense claim and wants to:
- Verify that all required documents are present
- Identify missing items before sending to finance
- Write a clear purpose description
- Avoid back-and-forth follow-up requests

Applicable to: petty cash, transportation, purchases, event costs, business meals, software subscriptions, travel and accommodation, advance payment requests.

### B.3 Required Data

1. Basic expense data: item, date, amount, currency, payment method, payer, department or project, purpose
2. Supporting documents: invoice, receipt, electronic invoice proof, card statement, bank transfer screenshot, order screenshot, contract or quote, event or travel approval record
3. Company rules: reimbursement deadline, document format requirements, company name or tax ID rules, approved expense types, manager approval threshold

### B.4 Assignment Template

```
Please help me check this expense reimbursement using the completeness check method.

Goal: Check whether the data is complete, what is missing, and what needs a clearer explanation. Do not decide whether the expense can be approved. Do not make the final call for finance.

Data:
[Expense item]
[Date]
[Amount and currency]
[Payment method]
[Payer]
[Department or project]
[Purpose]
[Documents provided]
[Company reimbursement rules]

Constraints:
- Do not make the final approval decision
- Do not promise the expense can be reimbursed
- Do not guess at documents not provided
- Do not ask for full credit card numbers, bank accounts, or ID numbers
- Flag sensitive fields (invoice number, card number) for masking
- Label anything insufficient as "to be supplemented / to be confirmed"

Output:
1. Reimbursement summary
2. Provided data
3. Missing items list (required / recommended / uncertain)
4. Items that need a clearer explanation
5. Items that may need manager approval
6. Pre-submission checklist
7. Suggested purpose statement text
8. Items finance needs to confirm
```

### B.5 Common Missing Items

- Missing invoice or receipt
- Missing payment proof
- Missing purpose description
- Missing project or department assignment
- Missing manager approval record
- Incorrect company name or tax ID
- Amount does not match payment screenshot
- Date exceeds reimbursement deadline

### B.6 Stop Conditions

AI should stop and flag for finance or manager review when:
- Documents appear incomplete or inconsistent
- Amount does not match the document
- Company name or tax ID is wrong
- Deadline has passed
- Personal and business expenses are mixed
- Large amounts involved
- Entertainment, gifts, commissions, or consulting fees
- Foreign currency or overseas payment
- Contract, procurement, or subscription renewal
- Tax questions
- Supplemental invoices or document amendments
- Unapproved purchases

### B.7 Verification Checklist

After using this skill, verify:
- Provided documents are clearly listed
- Missing items are clearly listed
- Finance has not been replaced as the final approver
- Sensitive data fields are flagged for masking
- Items needing manager or finance confirmation are labeled
- Purpose description matches actual use
- The output actually helps with pre-submission self-check

---

## Appendix C: Skill Example - Email Search and Attachment Safety Check

> This skill helps users organize email search conditions, identify candidate messages, check attachment risks, and produce a delivery checklist. The public edition does not recommend letting AI directly operate a private inbox, download attachments, or extract full message content. AI can only help organize search conditions and operating steps unless it has explicit authorization and connector access.

### C.1 Skill Name

`Email Search and Attachment Safety Check`

### C.2 Applicable Situations

Use when you know a specific email exists and need help:
- Organizing search conditions
- Deciding which keywords to use
- Comparing candidate messages against your criteria
- Checking attachment type and risk
- Preparing a delivery checklist before submitting documents as evidence or supporting files

Common use cases: e-invoice emails, receipt emails, platform order confirmations, payment notifications, vendor invoices, event registration confirmations, travel bookings, software subscription confirmations.

### C.3 Assignment Template

```
Please help me organize search conditions and a pre-delivery checklist for the following email.

Search clues:
- Sender:
- Subject keywords:
- Date range:
- Amount or order number:
- Content keywords:

I need:
1. Suggested search conditions organized
2. Candidate email matching criteria
3. What to mask before screenshotting the email
4. What risks to check before downloading the attachment
5. If the tool is authorized and capable, list the deliverable files

Constraints:
- Do not read or report unrelated email content
- Do not download suspicious attachments
- Do not click unknown links
- Do not output full credit card numbers, bank accounts, verification codes, or passwords
- If you do not have actual inbox access, clearly state you can only provide search and check steps
- If multiple similar emails are found, list candidates for me to confirm - do not choose for me
```

### C.4 Attachment Risk Checklist

Common acceptable attachment types: PDF, JPG, PNG, CSV, XLSX, receipt, invoice, order confirmation.

Before downloading, check:
- Is the attachment from a trusted sender?
- Does the file extension match what is expected?
- Is it a `.exe`, `.dmg`, suspicious `.zip`, or macro-enabled document?
- Does it require logging into an external website to access?
- Does it contain complete financial data or ID information?

AI must not:
- Ask for your email password or verification codes
- Click suspicious payment links
- Download `.exe`, `.dmg`, or unknown `.zip` files
- Read unrelated emails
- Paste full sensitive information into the conversation
- Forward emails to third parties
- Delete, archive, move, or flag emails without explicit instruction

### C.5 Stop Conditions

Stop and ask the user before continuing when:
- Multiple highly similar candidates are found
- Email contains sensitive personal data or full financial data
- Attachment type is suspicious
- Email looks like phishing
- Downloading requires logging into an external site
- Forwarding, deleting, archiving, or moving is needed
- Email content does not match what the user described

---

## Appendix D: Skill Example - Safe Computer Storage Cleanup

> The focus of this skill is safe read-only surveying and risk classification, not encouraging beginners to let AI delete files. Before any actual cleanup, back up first and confirm each item yourself. Stop immediately if company devices, cloud sync data, customer data, financial data, contracts, passwords, or system data are involved.

### D.1 Skill Name

`Safe Computer Storage Cleanup`

### D.2 Applicable Situations

Use when your computer is low on space and you want to:
- Find what is using the most storage
- Identify cleanup candidates safely
- Avoid downloading unknown cleanup software
- Know what is safe to delete and what absolutely must not be touched

Not suitable for:
- Suspected malware (needs IT security)
- Clearing company-confidential or personal data traces
- Reinstalling the system
- Bypassing company device management or permissions
- Asking AI to delete large amounts of data without confirmation

### D.3 The real risk with "free cleanup software"

Many cleanup tools that appear legitimate may request you to: download a `.dmg`, install a profile, enter your system password, grant full disk access, and then silently read your browser sessions, email, cloud storage, or saved credentials. The worst outcome is not a messy disk - it is losing account access, having cloud data compromised, or having work system permissions stolen.

Use a workspace AI agent to do a safe read-only survey first. Do not install unknown tools.

### D.4 Assignment Template

```
Please help me do a safe cleanup of low disk space.

Goal: Identify files and folders that can be safely cleaned up to free space, without affecting daily use, work projects, account security, or system stability.

Constraints:
- Do not delete any files yet
- Do not download or install any external cleanup software
- Do not touch passwords, browser data, email, cloud-synced folders, work projects, or system settings
- Do not use permanent deletion
- Do not assume "large file" or "not recently modified" means "safe to delete"
- Start with a read-only survey

Please output:
1. Current disk space remaining
2. Largest folders or file types
3. Low-risk candidates you recommend checking
4. Candidates that need my confirmation before touching
5. High-risk items that must not be touched
6. Estimated space that could be freed

Please output as a table: path, size, type, likely use, frequency (frequent / infrequent / unknown), suggested action, deletion risk, whether my confirmation is needed.
```

### D.5 Classification Rules

**Low-risk candidates (still need user confirmation):**
- Old installers, archives, and duplicate exports in the Downloads folder
- Screen recordings, meeting recordings, or temporary transcoded files you no longer need
- Caches and build artifacts that can be regenerated and do not affect login, sync, or project state
- Installer packages or exported reports that can be re-downloaded
- Temporary assets that have been delivered, backed up, and confirmed no longer needed

**Candidates that need confirmation:**
- Large video, image, or design asset files
- Old project folders
- Development build artifacts, simulator data, package caches
- Local copies of cloud-synced folders
- Compressed archives whose delivery or backup status is uncertain

**High-risk items - AI must not clean these without explicit instruction:**
- Passwords, Keychain, certificates, tokens, API keys
- Browser profiles, cookies, sessions, logged-in data
- Email, Messages, communication records
- Work projects, customer data, financial data, contracts, expense originals
- iCloud Drive, Google Drive, Dropbox, and other sync folders
- Application Support folders for apps whose purpose is unclear
- System folders, permission settings, device management data
- Photo libraries, music libraries, video editing project source files

### D.6 After user confirmation

Once the user confirms low-risk items, assign:

```
Please help me prepare the cleanup steps for the confirmed low-risk items.

Constraints:
- Do not delete anything yet
- List how each item will be handled, where it will go, and what might be affected
- Do not touch any path not in the confirmed list
- If a path does not exist or the content differs from the survey, stop and report
- After I confirm each item individually, I will decide whether to move it to the trash

Output:
1. Items recommended to move to trash
2. Size of each item
3. Reason for recommendation
4. Possible impact
5. Items I need to confirm or keep manually
```

**What this scenario is really teaching:**
> Do not install unknown software to solve a storage problem. Use a workspace AI agent to do a safe, read-only survey, then decide yourself what to remove.

AI's role is to help you understand where your space is going, classify cleanup candidates by risk, and avoid high-risk data. The final decision is always yours.

---

AI Work Assistant Handbook - Free Public Edition v1.0

Author: Farceur Liu | https://farceurliu.github.io/ai-butler-handbook/
