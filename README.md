Since you're asking for a **README.md**, I'll provide it as a reusable document you can directly place in your GitHub repository.

# 🛒 Agentic AI Shopping Assistant

## Building a Multi-Agent Personalized Shopping Recommendation System using LangGraph, LangChain, Groq LLM, Conversational Memory, Real-Time Product Retrieval, Deterministic Ranking, and Feedback-Driven Validation

---

# Table of Contents

1. Project Overview
2. Motivation
3. Problem Statement
4. Key Features
5. System Architecture
6. Technology Stack
7. Project Structure
8. Agent Workflow
9. LangGraph State Management
10. Memory Architecture
11. Planner Agent
12. Memory Agent
13. Researcher Agent
14. Product Retrieval Layer
15. Analyzer Agent
16. Recommendation Scoring Engine
17. Critic Agent
18. Feedback Loop Mechanism
19. LangGraph Workflow Construction
20. Complete Example Execution
21. Streamlit Frontend
22. LangSmith Observability
23. Challenges Faced
24. Design Decisions
25. Future Improvements
26. Skills Demonstrated
27. Conclusion

---

# Project Overview

The Agentic AI Shopping Assistant is an end-to-end multi-agent recommendation system designed to deliver personalized shopping recommendations through natural language conversations.

The system combines:

* Large Language Models (LLMs)
* Multi-Agent Architectures
* Conversational Memory
* Real-Time Product Retrieval
* Deterministic Recommendation Ranking
* Feedback-Based Validation

to create a shopping assistant capable of understanding user preferences, maintaining context across multiple interactions, retrieving live product data, ranking products intelligently, and generating explainable recommendations.

Unlike traditional chatbots that answer queries using a single prompt, this project decomposes the recommendation workflow into specialized agents that collaborate through a shared LangGraph state.

---

# Motivation

Modern LLMs are capable of recommending products through natural language interactions.

However, standalone LLMs suffer from several limitations:

### No Long-Term Memory

The model forgets user preferences after the conversation ends.

### No Structured Decision Making

Product recommendations are often based on probabilistic reasoning rather than explicit decision criteria.

### No Real-Time Product Access

Models cannot reliably retrieve up-to-date product information.

### Lack of Explainability

It is difficult to understand why a recommendation was selected.

### No Validation Layer

Recommendations may violate user constraints such as budget or preferred brands.

---

The objective of this project was to design a production-inspired AI system capable of solving these limitations through agent orchestration, memory management, retrieval augmentation, and deterministic ranking.

---

# Problem Statement

Build an intelligent shopping assistant capable of:

* Understanding shopping requirements
* Remembering user preferences
* Retrieving products in real time
* Ranking products according to constraints
* Generating natural language explanations
* Supporting follow-up conversations
* Validating recommendation quality

---

# Key Features

## Multi-Agent Workflow

Specialized agents collaborate to complete the recommendation process.

## Persistent User Memory

User preferences are automatically extracted and stored.

## Multi-Turn Conversations

Users can continue shopping conversations without repeating information.

## Real-Time Product Retrieval

Products are retrieved directly from Google Shopping.

## Deterministic Ranking

Recommendations are selected using explicit scoring rules.

## Recommendation Validation

A Critic Agent validates recommendations before they are shown.

## Explainable AI

The system explains why products were selected.

## Interactive Dashboard

Built using Streamlit.

## LangSmith Monitoring

Every agent execution is traceable.

---

# System Architecture

```text
                        User Query
                             │
                             ▼
                    Planner Agent
                             │
                             ▼
                     Memory Agent
                             │
                             ▼
                  Researcher Agent
                             │
                             ▼
                 Google Shopping API
                        (SerpAPI)
                             │
                             ▼
                    Analyzer Agent
                             │
                             ▼
                     Critic Agent
                             │
                             ▼
                  Final Recommendation
```

---

# Technology Stack

## AI Frameworks

* LangGraph
* LangChain
* LangSmith

## Language Model

* Groq
* Llama 3.3 70B Versatile

## Frontend

* Streamlit

## Retrieval Layer

* SerpAPI
* Google Shopping

## Programming Language

* Python

## Supporting Libraries

* Pandas
* Requests
* Dotenv
* UUID
* JSON
* Regex

---

# Project Structure

```text
shopping-assistant/
│
├── agents/
│   ├── planner.py
│   ├── memory.py
│   ├── researcher.py
│   ├── analyzer.py
│   └── critic.py
│
├── tools/
│   └── tools.py
│
├── graph.py
├── state.py
├── app.py
├── llm_config.py
├── store_factory.py
├── requirements.txt
│
└── README.md
```

---

# Agent Workflow

The system follows a sequential agentic workflow.

```text
Planner
   ↓
Memory
   ↓
Researcher
   ↓
Analyzer
   ↓
Critic
```

Each agent receives the current graph state, performs its task, updates the state, and passes control to the next agent.

---

# LangGraph State Management

The entire workflow is driven through a shared state object.

```python
class AgentState(TypedDict, total=False):

    user_input: str

    session_context: str

    products: List[dict]

    analysis: str

    next: str

    top_products: List[dict]

    comparison_table: List[dict]

    memory_text_list: List[str]

    retry_count: int
```

---

# Why TypedDict?

TypedDict provides a schema for the shared state.

Benefits:

* Type Safety
* Easier Debugging
* Better IDE Support
* Consistent State Structure

Every agent knows which fields can exist inside the workflow state.

---

# State Evolution Example

Initial State

```python
{
    "user_input":
    "JBL wireless headphones under 100 dollars"
}
```

After Planner

```python
{
    "user_input":
    "JBL wireless headphones under 100 dollars"
}
```

After Researcher

```python
{
    "user_input":
    "...",

    "products":
    [...]
}
```

After Analyzer

```python
{
    "products":
    [...],

    "top_products":
    [...],

    "analysis":
    "...",

    "comparison_table":
    [...]
}
```

After Critic

```python
{
    "next":
    "__end__"
}
```

LangGraph merges these updates into a single evolving state.

---

# Memory Architecture

The project distinguishes between:

## Workflow State

Temporary information used during a single graph execution.

Examples:

* Products
* Analysis
* Retry Count

---

## Long-Term Memory

Persistent user preferences stored across conversations.

Examples:

* Preferred Brand
* Budget
* Product Category

---

# Memory Storage Process

User Input

```text
I prefer JBL wireless headphones under 100 dollars
```

Memory Agent extracts:

```json
{
    "brand": "jbl",
    "budget": "100",
    "category": "wireless headphones"
}
```

Stored as:

```text
prefers brand jbl
budget 100
category wireless headphones
```

---

# Planner Agent

## Purpose

The Planner Agent is responsible for query refinement.

It transforms natural language shopping requests into cleaner and more structured retrieval queries.

Example:

Input:

```text
Can you suggest some good wireless headphones under 100 dollars?
```

Output:

```text
wireless headphones under 100 dollars
```

This reduces ambiguity before retrieval.

---

# Researcher Agent

## Purpose

The Researcher Agent performs shopping query generation and product retrieval.

It combines:

* Current User Query
* Stored Preferences
* Conversation Context

to generate an optimized search query.

Example:

Stored Memory:

```text
Brand: JBL
Budget: 100
Category: Wireless Headphones
```

Current Query:

```text
Show premium options
```

Generated Query:

```text
premium JBL wireless headphones under 100 dollars
```

---

# Product Retrieval Layer

The generated query is sent to SerpAPI.

SerpAPI acts as a bridge between the application and Google Shopping.

The actual product data comes from Google Shopping.

Retrieved Product Information:

```python
{
    "name": "...",
    "price": "...",
    "rating": "...",
    "image": "...",
    "link": "..."
}
```

---

# Analyzer Agent

## Purpose

The Analyzer Agent ranks products and selects the best recommendation.

Unlike many LLM applications, recommendation selection is not performed by the LLM.

Instead, a deterministic ranking engine is used.

Benefits:

* Consistency
* Explainability
* Reliability
* Easier Evaluation

---

# Recommendation Scoring Engine

Each product receives a score.

Formula:

Score =
Brand Match
+
Category Match
+
Budget Match
+
(2 × Rating)
------------

Missing Price Penalty

---

## Brand Match

Rewards products matching preferred brands.

Example:

```text
Preferred Brand = JBL
Product = JBL Tune 660NC
```

Bonus points awarded.

---

## Budget Match

Products closer to the user's budget receive higher scores.

Example:

```text
Budget = 100
Product Price = 95
```

Higher score.

---

## Rating Score

Higher rated products receive additional weight.

Example:

```text
Rating = 4.8
```

Contribution:

```text
2 × 4.8 = 9.6
```

---

# Recommendation Selection

Products are sorted by score.

Highest scoring product becomes:

```text
Best Product
```

Top three products are retained for comparison.

---

# Why Not Let The LLM Choose?

Deterministic Ranking:

* Repeatable
* Explainable
* Debuggable
* Evaluatable

Pure LLM Ranking:

* Non-Deterministic
* Expensive
* Difficult to Evaluate

Therefore:

Analyzer chooses the winner.

LLM explains the winner.

---

# Critic Agent

## Purpose

Acts as a recommendation quality validator.

The Critic verifies:

* Brand Constraints
* Budget Constraints

If violations are detected, retrieval is repeated.

---

# Feedback Loop

```text
Researcher
    ↓
Analyzer
    ↓
Critic
    ↓
Researcher
```

This creates a self-correcting recommendation workflow.

---

# Retry Protection

To prevent infinite loops:

```python
retry_count
```

is maintained in the graph state.

Maximum retries:

```text
2
```

---

# LangGraph Workflow Construction

Graph Initialization:

```python
builder = StateGraph(
    AgentState
)
```

Node Registration:

```python
builder.add_node(...)
```

Edge Creation:

```python
builder.add_edge(...)
```

Entry Point:

```python
builder.set_entry_point(
    "planner"
)
```

Compilation:

```python
graph = builder.compile(
    store=store
)
```

Execution:

```python
graph.invoke(
    state,
    config=config
)
```

---

# Complete Example Execution

User:

```text
I want JBL wireless headphones under 100 dollars
```

Planner:

```text
JBL wireless headphones under 100 dollars
```

Memory:

```json
{
    "brand":"JBL",
    "budget":"100",
    "category":"wireless headphones"
}
```

Researcher Query:

```text
JBL wireless headphones under 100 dollars
```

Retrieved Products:

```text
JBL Tune 660NC
Sony WH-CH720N
Anker Soundcore Q30
```

Analyzer Scores:

```text
JBL Tune 660NC     → 18.9
Sony WH-CH720N     → 15.2
Anker Q30          → 14.8
```

Critic:

```text
Validation Passed
```

Final Recommendation:

```text
JBL Tune 660NC
```

---

# Streamlit Frontend

The UI includes:

### AI Recommendation Section

Displays generated recommendation explanation.

### Product Comparison Table

Displays ranked products and scores.

### Product Cards

Shows:

* Product Image
* Product Name
* Price
* Rating
* Product Link

### Chat History

Stores previous interactions during the session.

---

# LangSmith Observability

Every agent is instrumented using:

```python
@traceable
```

This provides:

* Workflow Traces
* Agent Monitoring
* Performance Analysis
* Debugging Support

---

# Challenges Faced

* Designing memory extraction prompts
* Handling follow-up shopping queries
* Building deterministic ranking logic
* Integrating real-time shopping retrieval
* Managing shared graph state
* Preventing infinite feedback loops
* Maintaining recommendation consistency

---

# Future Improvements

* ChromaDB Integration
* Vector Search
* Hybrid Retrieval
* Product Embeddings
* RAG-Based Retrieval
* User Authentication
* PostgreSQL Memory Store
* Product Review Sentiment Analysis
* Cloud Deployment
* Multi-User Support
* Recommendation Evaluation Dashboard

---

# Skills Demonstrated

* Agentic AI
* LangGraph
* LangChain
* Multi-Agent Systems
* Conversational Memory
* State Management
* Recommendation Systems
* Retrieval-Augmented Applications
* Tool Calling
* Prompt Engineering
* Explainable AI
* Streamlit Development
* LangSmith Monitoring

---

# Conclusion

The Agentic AI Shopping Assistant demonstrates how modern AI systems can combine LLM reasoning, long-term memory, real-time retrieval, deterministic decision-making, and multi-agent collaboration to create personalized recommendation experiences. The project showcases key AI Engineering concepts including LangGraph workflows, stateful agent orchestration, memory management, retrieval integration, recommendation ranking, validation loops, and observability, making it a strong demonstration of practical Agentic AI system design.
