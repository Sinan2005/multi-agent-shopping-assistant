from typing import TypedDict, List

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