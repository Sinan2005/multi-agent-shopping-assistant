from langsmith import traceable
from langchain_groq import ChatGroq
from uuid import uuid4
import json

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

# -----------------------------------
# REMOVE OLD BRAND MEMORIES
# -----------------------------------
def remove_old_brand_preferences(
    store,
    user_id
):

    namespace = (
        "memories",
        user_id
    )

    memories = store.search(
        namespace
    )

    for m in memories:

        text = m.value[
            "data"
        ].lower()

        if "prefers brand" in text:

            store.delete(
                namespace,
                m.key
            )

# -----------------------------------
# SAVE MEMORY
# -----------------------------------
@traceable(name="Memory Extraction")
def save_memory(
    store,
    user_id,
    text
):

    extraction_prompt = f"""
Extract structured shopping preferences.

IMPORTANT:
- category must capture FULL product category.
- Examples:
    - gaming headphones
    - running shoes
    - wireless earbuds
    - gaming laptop

- Do NOT return vague categories like:
    - products
    - electronics
    - accessories

Return JSON ONLY.

Example:
{{
    "brand": "nike",
    "budget": "5000",
    "category": "running shoes"
}}

User Input:
{text}
"""

    response = llm.invoke(
        extraction_prompt
    ).content

    print(
        "MEMORY RESPONSE:",
        response
    )

    try:

        clean_response = (
            response
            .replace(
                "```json",
                ""
            )
            .replace(
                "```",
                ""
            )
            .strip()
        )

        data = json.loads(
            clean_response
        )

        print(
            "PARSED MEMORY:",
            data
        )

    except Exception as e:

        print(
            "MEMORY PARSE ERROR:",
            e
        )

        return

    namespace = (
        "memories",
        user_id
    )

    # -----------------------------------
    # BRAND MEMORY
    # -----------------------------------
    if data.get("brand"):

        remove_old_brand_preferences(
            store,
            user_id
        )

        print(
            "SAVING BRAND MEMORY"
        )

        store.put(
            namespace,
            str(uuid4()),
            {
                "data":
                f"prefers brand {data['brand']}"
            }
        )

    # -----------------------------------
    # BUDGET MEMORY
    # -----------------------------------
    if data.get("budget"):

        print(
            "SAVING BUDGET MEMORY"
        )

        store.put(
            namespace,
            str(uuid4()),
            {
                "data":
                f"budget {data['budget']}"
            }
        )

    # -----------------------------------
    # CATEGORY MEMORY
    # -----------------------------------
    if data.get("category"):

        print(
            "SAVING CATEGORY MEMORY"
        )

        store.put(
            namespace,
            str(uuid4()),
            {
                "data":
                f"category {data['category']}"
            }
        )

# -----------------------------------
# RETRIEVE MEMORIES
# -----------------------------------
@traceable(name="Retrieve Preferences")
def retrieve_preferences(
    store,
    user_id,
    query
):

    namespace = (
        "memories",
        user_id
    )

    memories = store.search(
        namespace
    )

    print(
        "RETRIEVED MEMORIES:"
    )

    for m in memories:

        print(
            m.value["data"]
        )

    return memories

# -----------------------------------
# LANGGRAPH MEMORY NODE
# -----------------------------------
@traceable(name="Memory Node")
def memory(
    state,
    config,
    store
):

    save_memory(
        store,
        config["configurable"]["user_id"],
        state["user_input"]
    )

    return {}