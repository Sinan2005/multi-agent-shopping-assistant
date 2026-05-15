from langchain_groq import ChatGroq
from agents.memory import retrieve_preferences
from langsmith import traceable
from llm_config import SYSTEM_PROMPT
import re

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

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

def sentiment_score(reviews):

    score = 0

    for r in reviews[:5]:

        r = r.lower()

        if "good" in r:
            score += 1

        if "bad" in r:
            score -= 1

    return score

def score_product(
    product,
    memories
):

    score = 0

    memory_text = [
        m.value["data"].lower()
        for m in memories
    ]

    for m in memory_text:

        if (
            "prefers" in m
            and product.get("name")
        ):

            brand = m.split(
                "prefers"
            )[1].split()[0]

            if brand in product[
                "name"
            ].lower():

                score += 3

    budget = extract_budget(
        memory_text
    )

    price = parse_price(
        product.get("price")
    )

    if budget and price:

        score += max(
            0,
            5 - abs(
                budget - price
            ) / 1000
        )

    if product.get("rating"):

        score += float(
            product["rating"]
        )

    return score

@traceable(name="Analyzer Agent")
def analyzer(
    state,
    config,
    store
):

    print("Analyzer running")

    memories = retrieve_preferences(
        store,
        config["configurable"]["user_id"],
        state["user_input"]
    )

    scored = [
        (
            p,
            score_product(
                p,
                memories
            )
        )
        for p in state["products"]
    ]

    scored.sort(
        key=lambda x: x[1],
        reverse=True
    )

    top_products = [
        p for p, _ in scored[:3]
    ]

    comparison_table = []

    for p, s in scored[:3]:

        comparison_table.append({
            "Product": p.get("name"),
            "Price": p.get("price"),
            "Rating": p.get("rating"),
            "Score": round(s, 2),
            "Link": p.get("link")
        })

    memory_text = "\n".join([
        m.value["data"]
        for m in memories
    ])

    response = llm.invoke([
        ("system", SYSTEM_PROMPT),
        ("human", f"""
You are an AI shopping recommendation expert.

Analyze products and recommend the BEST option.

User Preferences:
{memory_text}

Products:
{top_products}

Instructions:
- Keep response concise.
- Avoid long paragraphs.
- Focus on practical recommendation quality.
- Do NOT repeat unnecessary details.
- Mention only relevant comparisons.
- Avoid generic disclaimers.

Return output in EXACTLY this format:

Best Product:
<product name>

Price:
<price>

Why Recommended:
- point 1
- point 2
- point 3

Final Verdict:
<1 short concluding sentence>
""")
    ]).content

    return {
        "analysis": response,
        "top_products": top_products,
        "comparison_table": comparison_table,
        "memory_text_list": [
            m.value["data"]
            for m in memories
        ]
    }