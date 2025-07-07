import streamlit as st
import random
from pages.qa_data import questions as qa_collection
from scentmatch.graph import graph
from scentmatch.configuration import Configuration

if "result" not in st.session_state:
    if "selected_questions" not in st.session_state:
        st.session_state.selected_questions = random.sample(list(qa_collection.keys()), 3)

    questions = st.session_state.selected_questions
    answers = [qa_collection[question] for question in questions]

    st.title("Legendary Scent Match")

    st.markdown("""
    This app lets you run Scent Match workflows.
    """)

    st.write("Please answer the following questions to find your perfect scent.")

    user_responses = {}

    for question, answer in zip(questions, answers):
        user_responses[question] = st.radio(question, answer, index=None)

    user_answers = [answer for _, answer in user_responses.items() if answer is not None]

    if st.button("Find your perfect scent!"):
        # check if user has answered all questions
        if len(user_answers) == len(questions):
            st.write("Your perfect scent is...")
            with st.spinner("Processing..."):
                with st.empty():
                    input_data = {"about_user": user_responses}
                    config_ = Configuration()
                    for stream_mode, chunk in graph.stream(
                        input_data,
                        config={
                            "configurable": {
                                "thread_id": "1",
                                "available_products": config_.available_products,
                                "model": config_.model,
                            }
                        },
                        stream_mode=["values", "custom"],
                    ):
                        if stream_mode == "custom":
                            st.write(chunk.get("custom_key", ""))
                        elif stream_mode == "values":
                            result = chunk
                            st.write("")
                    st.session_state["result"] = result["sales_pitch"]
            # st.write(user_responses)
            # st.write(st.session_state["result"])
            st.rerun()
        else:
            st.error("Please answer all questions to find your perfect scent.")

else:
    st.write(st.session_state["result"])
