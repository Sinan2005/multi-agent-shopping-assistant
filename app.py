from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import pandas as pd

from graph import graph
from langsmith import traceable

st.set_page_config(
    page_title="AI Budget Shopping Assistant",
    page_icon="🛒",
    layout="wide"
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🛒 AI Budget Shopping Assistant")

@traceable(name="Full Graph Run")
def run(state, config):

    return graph.invoke(
        state,
        config=config
    )

query = st.text_input(
    "What do you want?"
)

if st.button("Find Best"):

    st.write("Running graph...")

    config = {
        "configurable": {
            "user_id": "u1"
        }
    }

    state = {
        "user_input": query,
        "products": [],
        "analysis": "",
        "retry_count": 0
    }

    result = run(
        state,
        config
    )

    st.session_state.chat_history.append({
        "query": query,
        "response": result["analysis"]
    })

    st.success("Recommendation Generated")

    st.subheader("📊 AI Recommendation")

    st.write(
        result["analysis"]
    )

    st.subheader("📋 Product Comparison")

    comparison_data = result.get(
        "comparison_table",
        []
    )

    df = pd.DataFrame(
        comparison_data
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("🛍️ Top Products")

    cols = st.columns(3)

    for col, product in zip(
        cols,
        result["top_products"]
    ):

        with col:

            if product.get("image"):

                st.image(
                    product["image"],
                    width=200
                )

            st.markdown(
                f"""
### {product.get('name')}

💰 Price: {product.get('price')}

⭐ Rating: {product.get('rating')}
                """
            )

            if product.get("link"):

                st.link_button(
                    "View Product",
                    product["link"]
                )

st.subheader("🕘 Chat History")

for chat in reversed(
    st.session_state.chat_history
):

    with st.expander(
        chat["query"]
    ):

        st.write(
            chat["response"]
        )