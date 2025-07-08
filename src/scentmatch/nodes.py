from scentmatch.state import WorkflowState
from scentmatch.configuration import Configuration
import random
from langchain.chat_models import init_chat_model
import os


def sales_node(state: WorkflowState, config: Configuration):
    user_response = "\n".join(f"{k}: {v}" for k, v in state["about_user"].items())

    # Get the available products from the config
    available_products = config["configurable"]["available_products"]
    chosen_product = random.choice(available_products)
    product_description = os.path.join(
        "products", chosen_product + ".txt"
    )
    with open(product_description, "r") as f:
        product_description = f.read()

    # Get the prompt from the file
    prompt = os.path.join("products", "sales_prompt.txt")
    with open(prompt, "r") as f:
        prompt = f.read()
    sales_prompt = prompt.format(
        user_response=user_response, product_description=product_description
    )

    llm = init_chat_model(config["configurable"]["model"], temperature=1)
    sales_pitch = llm.invoke(sales_prompt)

    return {"sales_pitch": sales_pitch.content, "chosen_product": chosen_product}
