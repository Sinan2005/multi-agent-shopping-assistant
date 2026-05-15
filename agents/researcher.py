from tools.tools import search_products
from agents.memory import retrieve_preferences
from langsmith import traceable

@traceable(name="Researcher Agent")
def researcher(
    state,
    config,
    store
):

    print("Researcher running")

    memories = retrieve_preferences(
        store,
        config["configurable"]["user_id"],
        state["user_input"]
    )

    brand = ""
    budget = ""
    category = ""

    for m in memories:

        text = m.value["data"].lower()

        if "prefers brand" in text:

            brand = text.replace(
                "prefers brand",
                ""
            ).strip()

        elif "budget" in text:

            budget = text.replace(
                "budget",
                ""
            ).strip()

        elif "category" in text:

            category = text.replace(
                "category",
                ""
            ).strip()

    user_input = state[
        "user_input"
    ].lower()

    # BRAND SWITCH HANDLING
    if "switch to" in user_input:

        words = user_input.split()

        if len(words) >= 3:

            brand = words[-1]

    query_parts = []

    # FOLLOW-UP INTENT FLAGS
    is_premium = (
        "premium" in user_input
    )

    is_cheaper = (
        "cheap" in user_input
        or "cheaper" in user_input
    )

    is_better = (
        "better rated" in user_input
        or "top rated" in user_input
    )

    # FOLLOW-UP QUERY REFINEMENT

    if is_premium:
        query_parts.append(
            "premium"
        )

    if is_cheaper:
        query_parts.append(
            "cheap"
        )

    if is_better:
        query_parts.append(
            "top rated"
        )

    # ALWAYS PRESERVE BRAND
    if brand:
        query_parts.append(
            brand
        )

    # ALWAYS PRESERVE CATEGORY
    if category:
        query_parts.append(
            category
        )

    # ALWAYS PRESERVE BUDGET
    if budget:
        query_parts.append(
            f"under {budget}"
        )

    # FALLBACK
    if not category:
        query_parts.append(
            "shopping products"
        )

    final_query = " ".join(
        query_parts
    )

    print(
        "FINAL QUERY:",
        final_query
    )

    products = search_products(
        final_query
    )

    return {
        "products": products
    }