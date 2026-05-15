from langsmith import traceable

@traceable(name="Decision Agent")
def decision(state):

    print("Decision running")

    products = state.get("products", [])

    print("Products count:", len(products))

    if len(products) == 0:

        return {
            "next": "analyzer"
        }

    return {
        "next": "analyzer"
    }