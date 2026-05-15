from langchain_groq import ChatGroq
from langsmith import traceable
from llm_config import SYSTEM_PROMPT
from dotenv import load_dotenv
load_dotenv()
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

@traceable(name="Planner Agent")
def planner(state):
    print("Planner running")

    query = state["user_input"]

    context = state.get(
        "session_context",
        ""
    )

    refined = llm.invoke([
        ("system", SYSTEM_PROMPT),
        ("human", f"""
You are a shopping query planning agent.

Your task is to transform the user's shopping request into a clean,
specific, searchable shopping query.

Instructions:
- Understand the user's intent carefully.
- Preserve:
    - brand preferences
    - category
    - budget
    - constraints
- Combine previous context with latest query.
- Prioritize latest user preference.
- Remove ambiguity.
- Optimize for product search.

Conversation Context:
{context}

User Query:
{query}

Return ONLY the refined shopping query.
""")
    ]).content

    return {
        "user_input": refined
    }