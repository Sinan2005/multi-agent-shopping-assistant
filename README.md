# 🛒 Agentic AI Shopping Assistant

## Overview

The Agentic AI Shopping Assistant is an end-to-end multi-agent recommendation system that combines Large Language Models (LLMs), conversational memory, real-time product retrieval, deterministic ranking, and feedback-driven validation to deliver personalized shopping recommendations.

The system is built using LangGraph and follows an agentic workflow in which specialized agents collaborate to understand user requirements, remember shopping preferences, retrieve relevant products from Google Shopping, rank recommendations based on user constraints, validate recommendation quality, and generate natural-language explanations.

Unlike traditional recommendation systems that rely solely on collaborative filtering or static ranking algorithms, this project combines LLM reasoning with deterministic decision-making to create an explainable and context-aware shopping assistant.

---

# Motivation

Modern LLMs can recommend products through natural conversation, but they often lack:

* Persistent user memory
* Structured decision-making
* Transparent recommendation logic
* Constraint validation
* Real-time product retrieval

This project was designed to address these limitations by building an agentic architecture capable of:

* Remembering user preferences
* Understanding follow-up queries
* Retrieving live products
* Applying deterministic ranking logic
* Validating recommendations before presenting results

The goal was not simply to build another chatbot, but to explore AI Engineering concepts such as:

* Multi-Agent Systems
* LangGraph Workflows
* Conversational Memory
* Retrieval-Augmented Applications
* Explainable Recommendation Systems
* State Management
* Human-like Shopping Assistance

---

# Key Features

### Multi-Agent Architecture

The system is composed of specialized agents with distinct responsibilities.

### Persistent Shopping Memory

User preferences are automatically extracted and stored.

### Multi-Turn Conversations

Users can refine recommendations without repeating preferences.

### Real-Time Product Retrieval

Products are retrieved from Google Shopping using SerpAPI.

### Deterministic Ranking

Recommendations are selected using explicit scoring rules rather than purely relying on LLM output.

### Recommendation Validation

A Critic Agent validates recommendations and triggers retries when constraints are violated.

### Explainable Recommendations

The system explains why a product was selected.

### Interactive Frontend

Built with Streamlit for easy interaction and visualization.

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

The workflow is orchestrated using LangGraph where each agent operates as a node in a stateful graph.

---

# Technology Stack

## AI Frameworks

* LangGraph
* LangChain
* LangSmith

## Language Model

* Groq
* Llama 3.3 70B Versatile

## Retrieval Layer

* SerpAPI
* Google Shopping

## Frontend

* Streamlit

## Backend

* Python

## Supporting Libraries

* Pandas
* Requests
* Dotenv
* JSON
* Regex
* UUID

---

# Workflow Walkthrough

## Step 1: User Interaction

The workflow begins when a user submits a shopping request.

Example:

```text
I need JBL wireless headphones under 100 dollars.
```

The request enters the LangGraph workflow.

---

# Planner Agent

## Purpose

The Planner Agent acts as the workflow entry point.

Its objective is to convert user requests into cleaner and more structured shopping queries.

## Responsibilities

* Understand user intent
* Remove ambiguity
* Preserve user constraints
* Generate search-ready queries

## Example

Input:

```text
Can you suggest some good wireless headphones under 100 dollars?
```

Output:

```text
wireless headphones under 100 dollars
```

This refined query is passed to downstream agents.

---

# Memory Agent

## Purpose

The Memory Agent extracts structured shopping preferences from user interactions and stores them in a persistent memory store.

## Extracted Preferences

* Preferred Brand
* Budget
* Product Category

## Example

Input:

```text
I prefer JBL wireless headphones under 100 dollars.
```

Extracted JSON:

```json
{
    "brand": "JBL",
    "budget": "100",
    "category": "wireless headphones"
}
```

These preferences become available for future conversations.

---

## Why Memory Matters

Without memory:

```text
User:
Show premium options.
```

The system lacks context.

With memory:

```text
Brand = JBL
Budget = 100
Category = Wireless Headphones
```

The system understands:

```text
premium JBL wireless headphones under 100 dollars
```

This enables personalized multi-turn conversations.

---

# Researcher Agent

## Purpose

The Researcher Agent is responsible for product discovery and retrieval.

It combines:

* Current user query
* Stored preferences
* Conversation context

to create an optimized shopping search query.

## Example

Stored Memory:

```text
Brand: JBL
Budget: 100
Category: Wireless Headphones
```

User Query:

```text
Show me premium options.
```

Generated Search Query:

```text
premium JBL wireless headphones under 100 dollars
```

---

# Real-Time Retrieval Layer

The generated query is sent to Google Shopping via SerpAPI.

## Why SerpAPI?

Direct scraping is difficult and unreliable.

SerpAPI provides:

* Structured JSON responses
* Stable API interface
* Google Shopping access
* Product metadata extraction

---

# Data Source

The actual product data comes from:

Google Shopping

SerpAPI acts as a retrieval interface between the application and Google Shopping.

---

# Retrieved Product Information

Each product includes:

```python
{
    "name": "...",
    "price": "...",
    "rating": "...",
    "image": "...",
    "link": "..."
}
```

These products are stored inside the graph state.

---

# Analyzer Agent

## Purpose

The Analyzer Agent performs recommendation ranking.

Rather than allowing the LLM to choose products directly, a deterministic scoring engine is used.

This improves:

* Consistency
* Explainability
* Reliability
* Evaluation

---

# Product Ranking Formula

The recommendation score is calculated using:

Brand Match

*

Category Match

*

Budget Match

*

2 × Product Rating

*

Missing Price Penalty

---

## Brand Match

Rewards products matching the preferred brand.

Example:

```text
Preferred Brand: JBL
Product: JBL Tune 660NC
```

Bonus score applied.

---

## Category Match

Rewards products matching the preferred category.

Example:

```text
Category: Wireless Headphones
```

Products containing relevant category keywords receive additional points.

---

## Budget Match

Products closer to the user's budget receive higher scores.

Example:

```text
Budget = 100
Product Price = 95
```

Results in a strong budget-fit score.

---

## Rating Score

Higher-rated products receive additional weight.

Example:

```text
Rating = 4.7
```

Contributes positively to the overall score.

---

# Recommendation Selection

After scoring all retrieved products:

1. Products are sorted.
2. Highest scoring product is selected.
3. Top 3 products are preserved.
4. Comparison table is generated.

---

# Why Not Let The LLM Choose?

The project intentionally separates:

Recommendation Selection

from

Recommendation Explanation

Benefits:

* Deterministic behavior
* Easier debugging
* Easier evaluation
* Lower inference cost
* Better reproducibility

The LLM is used only to explain the recommendation.

---

# Critic Agent

## Purpose

Acts as a quality assurance layer.

The Critic verifies whether recommendations satisfy user constraints.

## Validation Checks

### Budget Constraint

Checks whether retrieved products exceed the user's budget.

### Brand Constraint

Checks whether products satisfy preferred brand requirements.

---

# Feedback Loop

If violations are detected:

```text
Analyzer
    ↓
Critic
    ↓
Researcher
```

The query is refined and retrieval is repeated.

This creates a self-correcting workflow.

---

# Retry Protection

A retry counter prevents infinite loops.

Maximum retries:

```text
2
```

---

# LangGraph State

The graph uses a shared state object.

```python
{
    "user_input": "",
    "products": [],
    "top_products": [],
    "analysis": "",
    "comparison_table": [],
    "memory_text_list": [],
    "retry_count": 0
}
```

Each agent reads and updates portions of the state.

---

# State Evolution Example

Initial State:

```python
{
    "user_input":
    "JBL headphones under 100 dollars"
}
```

After Researcher:

```python
{
    "products": [...]
}
```

After Analyzer:

```python
{
    "top_products": [...],
    "analysis": "...",
    "comparison_table": [...]
}
```

After Critic:

```python
{
    "next": "__end__"
}
```

---

# Streamlit Interface

The frontend includes:

### AI Recommendation Summary

Natural-language recommendation generated by the Analyzer.

### Product Comparison Table

Displays ranked products and scores.

### Product Cards

Includes:

* Product Image
* Product Name
* Price
* Rating
* Product Link

### Chat History

Maintains interaction history during the session.

---

# LangSmith Observability

LangSmith is used to monitor:

* Agent Execution
* Workflow Traces
* Node-Level Performance
* Debugging
* Development Testing

Every agent is instrumented using:

```python
@traceable
```

allowing complete workflow visibility.

---

# Future Enhancements

Planned improvements include:

* Vector Database Integration
* ChromaDB
* Hybrid Retrieval
* Product Embeddings
* Semantic Search
* Evaluation Dashboards
* RAGAS Integration
* User Authentication
* PostgreSQL Memory Store
* Multi-User Support
* Cloud Deployment
* Product Review Sentiment Analysis

---

# Skills Demonstrated

This project showcases practical experience in:

* Agentic AI
* Multi-Agent Systems
* LangGraph
* LangChain
* LLM Applications
* Retrieval Systems
* Conversational Memory
* State Management
* Recommendation Systems
* Prompt Engineering
* Tool Integration
* Explainable AI
* Streamlit Development
* LangSmith Monitoring

---

# Conclusion

The Agentic AI Shopping Assistant demonstrates how modern AI systems can combine LLM reasoning, memory, retrieval, deterministic decision-making, and agent collaboration to create personalized and explainable recommendation experiences. The project serves as a practical exploration of AI Engineering principles and showcases the design of production-inspired agentic workflows using LangGraph and LangChain.
