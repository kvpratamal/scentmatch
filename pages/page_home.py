import streamlit as st
import os
import uuid
from scentmatch.graph import chat_graph
from scentmatch.configuration import Configuration
from langchain.schema import HumanMessage, AIMessage


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
    cols = st.columns(3)
    with cols[1]:
        st.image(f"products/{product}.jpg", use_container_width=True)

    if (
        "messages" not in st.session_state
        or st.session_state.get("product_in_chat") != product
    ):
        st.session_state.messages = [
            AIMessage(content=f"Hello! Ask me anything about {product}!")
        ]
        st.session_state.product_in_chat = product

    avatars = {
        "user": "😊",
        "assistant": "✨",
    }

    for message in st.session_state.messages:
        if isinstance(message, HumanMessage):
            with st.chat_message("user", avatar=avatars["user"]):
                st.markdown(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant", avatar=avatars["assistant"]):
                st.markdown(message.content)

    if prompt := st.chat_input(f"Ask something about {product}"):
        st.session_state.messages.append(HumanMessage(content=prompt))
        with st.chat_message("user", avatar=avatars["user"]):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=avatars["assistant"]):
            with st.spinner("*Scenting out the perfect answer...*"):
                message_placeholder = st.empty()
                full_response = ""
                input_data = {"question": prompt, "product": product}
                config_ = Configuration(
                    model="google_genai:gemini-2.5-flash-lite-preview-06-17",
                    thread_id=st.session_state.session_id,
                )
                config_dict = config_.model_dump()
                stop = False
                for chunk in chat_graph.stream(
                    input_data,
                    config=config_dict,
                    stream_mode="messages",
                ):
                    if not stop:
                        full_response += chunk[0].content
                        message_placeholder.markdown(full_response)
                    if (
                        "finish_reason" in chunk[0].response_metadata
                        and chunk[0].response_metadata["finish_reason"] == "STOP"
                    ):
                        stop = True
                st.session_state.messages.append(AIMessage(content=full_response))
