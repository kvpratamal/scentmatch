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
                    st.session_state["result"] = result
            st.rerun()
        else:
            st.error("Please answer all questions to find your perfect scent.")

else:
    # Retrieve data from session state
    chosen_product = st.session_state["result"]["chosen_product"]
    sales_pitch = st.session_state["result"]["sales_pitch"]

    # Split sales pitch into parts
    sentences = [s.strip() for s in sales_pitch.split(".") if s.strip()]
    first_sentence = sentences[0]
    intermediate_sentences = sentences[1:-1]
    last_sentence = sentences[-1] if len(sentences) > 1 else ""

    # Load CSS from external file
    def load_css(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    load_css('pages/styles.css')

    # Header with beautiful styling
    st.markdown(f'<div class="main-title sparkle">🌟 Your Perfect Scent: <br> {chosen_product} </div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">💬 {first_sentence}</div>', unsafe_allow_html=True)

    # Create spacer
    st.markdown("<br>", unsafe_allow_html=True)

    # Layout: description on the left, image on the right
    st.markdown('<h3 class="section-title">✨ Why You\'ll Love It</h3>', unsafe_allow_html=True)
    cols = st.columns([1.2, 1])


    with cols[0]:
        for i, sentence in enumerate(intermediate_sentences):
            emoji = ["💖", "🌸", "✨", "🎯", "🌟", "💫", "🔮", "🌺"][i % 8]
            st.markdown(f'<div class="feature-item">{emoji} {sentence.strip()}.</div>', unsafe_allow_html=True)

    with cols[1]:
        st.image(f"imgs/{chosen_product}.jpg", use_container_width=True, caption=f"✨ {chosen_product} ✨")

    # Add final sentence as a closing highlight
    if last_sentence:
        st.markdown(f'<div class="closing-highlight sparkle">🌸 {last_sentence} 🌸</div>', unsafe_allow_html=True)

    # Add some extra visual flair
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem; opacity: 0.7;">
        <span style="font-size: 1.5rem;">✨ 🌟 ✨ 🌟 ✨</span>
    </div>
    """, unsafe_allow_html=True)
    
