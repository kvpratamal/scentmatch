import streamlit as st
import os
import uuid
from scentmatch.graph import chat_graph
from scentmatch.configuration import Configuration


# Load CSS from external file
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("pages/styles.css")

if "session_id" not in st.session_state:
    st.session_state.session_id = uuid.uuid4().hex

# Logo at the top
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("products/logo.png", use_container_width=True)


def get_products():
    products = []
    for item in os.listdir("products"):
        if item.endswith(".jpg"):
            products.append(item.replace(".jpg", ""))
    return products


products = get_products()

if "selected_product" not in st.session_state:
    st.markdown(
        '<h1 class="main-title sparkle">🌟 Select a Product 🌟</h1>',
        unsafe_allow_html=True,
    )

    # Display products in a grid
    cols = st.columns(3)
    for i, product in enumerate(products):
        with cols[i % 3]:
            st.image(f"products/{product}.jpg", use_container_width=True)
            if st.button(product, key=f"product_{product}"):
                st.session_state.selected_product = product
                st.rerun()

else:
    product = st.session_state.selected_product
    st.markdown(
        f'<h1 class="main-title sparkle">🌟 Chat with {product} 🌟</h1>',
        unsafe_allow_html=True,
    )

    if (
        "messages" not in st.session_state
        or st.session_state.get("product_in_chat") != product
    ):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": f"Hello! Ask me anything about {product}!",
            }
        ]
        st.session_state.product_in_chat = product

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask something about the product"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            input_data = {"question": prompt, "product": product}
            config_ = Configuration()
            for stream_mode, chunk in chat_graph.stream(
                input_data,
                config={
                    "configurable": {
                        "thread_id": st.session_state.session_id,
                        "model": config_.model,
                    }
                },
                stream_mode=["values", "custom"],
            ):
                if stream_mode == "values":
                    full_response += chunk.get("response", "")
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
