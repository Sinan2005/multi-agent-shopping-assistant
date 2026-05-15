from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph

from state import AgentState
from store_factory import get_store

from agents.planner import planner
from agents.researcher import researcher
from agents.decision import decision
from agents.analyzer import analyzer
from agents.critic import critic
from agents.memory import memory

# -----------------------------------
# STORE
# -----------------------------------
store = get_store()

# -----------------------------------
# GRAPH BUILDER
# -----------------------------------
builder = StateGraph(
    AgentState
)

# -----------------------------------
# NODES
# -----------------------------------
builder.add_node(
    "planner",
    planner
)

builder.add_node(
    "memory",
    memory
)

builder.add_node(
    "researcher",
    researcher
)

builder.add_node(
    "decision",
    decision
)

builder.add_node(
    "analyzer",
    analyzer
)

builder.add_node(
    "critic",
    critic
)

# -----------------------------------
# ENTRY POINT
# -----------------------------------
builder.set_entry_point(
    "planner"
)

# -----------------------------------
# EDGES
# -----------------------------------

# Planner → Memory
builder.add_edge(
    "planner",
    "memory"
)

# Memory → Researcher
builder.add_edge(
    "memory",
    "researcher"
)

# Researcher → Decision
builder.add_edge(
    "researcher",
    "decision"
)

# Decision Routing
builder.add_conditional_edges(
    "decision",
    lambda x: x["next"],
    {
        "researcher": "researcher",
        "analyzer": "analyzer"
    }
)

# Analyzer → Critic
builder.add_edge(
    "analyzer",
    "critic"
)

# Critic Routing
builder.add_conditional_edges(
    "critic",
    lambda x: x["next"],
    {
        "researcher": "researcher",
        "__end__": "__end__"
    }
)

# -----------------------------------
# COMPILE
# -----------------------------------
graph = builder.compile(
    store=store
)