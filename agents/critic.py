import re
from langsmith import traceable

def parse_price(price):

    nums = re.findall(
        r"\d+",
        str(price)
    )

    if nums:
        return int(
            "".join(nums)
        )

    return None

def extract_budget(memories):

    for m in memories:

        if "budget" in m.lower():

            nums = re.findall(
                r"\d+",
                m
            )

            if nums:
                return int(nums[0])

    return None

def extract_brand(memories):

    for m in memories:

        if "prefers brand" in m.lower():

            return m.lower().replace(
                "prefers brand",
                ""
            ).strip()

    return None

@traceable(name="Critic Agent")
def critic(state):

    budget = extract_budget(
        state.get(
            "memory_text_list",
            []
        )
    )

    brand = extract_brand(
        state.get(
            "memory_text_list",
            []
        )
    )

    violations = []

    for p in state.get(
        "top_products",
        []
    ):

        if budget:

            price = parse_price(
                p.get("price")
            )

            if (
                price
                and price > budget
            ):

                violations.append(
                    "budget"
                )

    if brand:

        found = any(
            brand in (
                p.get("name") or ""
            ).lower()
            for p in state[
                "top_products"
            ]
        )

        if not found:

            violations.append(
                "brand"
            )

    if violations:

        retry_count = state.get(
            "retry_count",
            0
        )

        if retry_count >= 2:

            return {
                "next": "__end__"
            }

        refined_query = state[
            "user_input"
        ]

        if budget:
            refined_query += (
                f" under {budget}"
            )

        if brand:
            refined_query += (
                f" {brand}"
            )

        return {
            "user_input": refined_query,
            "retry_count": retry_count + 1,
            "next": "researcher"
        }

    return {
        "next": "__end__"
    }