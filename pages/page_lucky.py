import streamlit as st
import random
import uuid
from products.qa_data import questions as qa_collection
from scentmatch.graph import graph
from scentmatch.configuration import Configuration
from scentmatch.translator import translate


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

if "result" not in st.session_state:
    if "selected_questions" not in st.session_state:
        st.session_state.selected_questions = random.sample(
            list(qa_collection.keys()), 3
        )

    questions = st.session_state.selected_questions
    answers = [qa_collection[question] for question in questions]

    # Enhanced title with decorative elements
    st.markdown(
        f'<h1 class="main-title sparkle">{translate("lucky.title")}</h1>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'''
    <div class="subtitle">
        {translate("lucky.subtitle")}
    </div>
    ''',
        unsafe_allow_html=True,
    )

    # Feature badges
    st.markdown(
        f'''
    <div style="text-align: center; margin-bottom: 2rem;">
        <span class="feature-badge">{translate("lucky.badge_personalized")}</span>
        <span class="feature-badge">{translate("lucky.badge_premium")}</span>
        <span class="feature-badge">{translate("lucky.badge_ai_powered")}</span>
        <span class="feature-badge">{translate("lucky.badge_instant_results")}</span>
    </div>
    ''',
        unsafe_allow_html=True,
    )

    # Decorative divider
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Questions container
    # st.markdown('<div class="question-container">', unsafe_allow_html=True)

    st.markdown(
        f'''
    <h2 style="text-align: center; color: #2d3748; margin-bottom: 2rem; font-size: 2rem;">
        {translate("lucky.preferences_title")}
    </h2>
    ''',
        unsafe_allow_html=True,
    )

    user_responses = {}

    for i, (question, answer) in enumerate(zip(questions, answers), 1):
        # st.markdown(f'<div class="question-item">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="question-title">{translate("lucky.question_title", i=i, question=question)}</div>',
            unsafe_allow_html=True,
        )
        user_responses[question] = st.radio(
            f"Select your answer for question {i}:",
            answer,
            index=None,
            key=f"question_{i}",
            label_visibility="hidden",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Progress indicator
    user_answers = [
        answer for _, answer in user_responses.items() if answer is not None
    ]
    progress = len(user_answers) / len(questions) * 100

    st.markdown(
        f'''
    <div class="progress-indicator">
        {translate("lucky.progress", answered=len(user_answers), total=len(questions), percent=progress)}
        <div style="background: rgba(102, 126, 234, 0.3); height: 8px; border-radius: 4px; margin-top: 0.5rem;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); height: 100%; width: {progress}%; border-radius: 4px; transition: width 0.3s ease;"></div>
        </div>
    </div>
    ''',
        unsafe_allow_html=True,
    )

    # Enhanced button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(translate("lucky.find_scent_button"), key="find_scent_button"):
            # check if user has answered all questions
            if len(user_answers) == len(questions):
                st.markdown(
                    f'''
                <div style="text-align: center; font-size: 1.5rem; color: #667eea; margin: 2rem 0;">
                    {translate("lucky.analyzing")}
                </div>
                ''',
                    unsafe_allow_html=True,
                )

                with st.spinner(translate("lucky.creating_profile")):
                    with st.empty():
                        input_data = {"about_user": user_responses}
                        config_ = Configuration()
                        for stream_mode, chunk in graph.stream(
                            input_data,
                            config={
                                "configurable": {
                                    "thread_id": st.session_state.session_id,
                                    "available_products": config_.available_products,
                                    "language": config_.language,
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
                st.error(
                    translate("lucky.error_all_questions")
                )

    # Footer with decorative elements
    st.markdown(
        f'''
    <div style="text-align: center; margin-top: 3rem; padding: 2rem; color: #666;">
        <p style="font-style: italic;">{translate("lucky.footer_perfect_scent")}</p>
    </div>
    ''',
        unsafe_allow_html=True,
    )

else:
    # Retrieve data from session state
    chosen_product = st.session_state["result"]["chosen_product"]
    sales_pitch = st.session_state["result"]["sales_pitch"]

    # Split sales pitch into parts
    sentences = [s.strip() for s in sales_pitch.split(".") if s.strip()]
    first_sentence = sentences[0]
    intermediate_sentences = sentences[1:-1]
    last_sentence = sentences[-1] if len(sentences) > 1 else ""

    # Header with beautiful styling
    st.markdown(
        f'<div class="main-title sparkle">{translate("lucky.perfect_scent", product=chosen_product)}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="subtitle">💬 {first_sentence}</div>', unsafe_allow_html=True
    )

    # Create spacer
    st.markdown("<br>", unsafe_allow_html=True)

    # Layout: description on the left, image on the right
    st.markdown(
        f'<h3 class="section-title">{translate("lucky.why_you_love_it")}</h3>',
        unsafe_allow_html=True,
    )
    cols = st.columns([1.2, 1])

    with cols[0]:
        for i, sentence in enumerate(intermediate_sentences):
            emoji = ["💖", "🌸", "✨", "🎯", "🌟", "💫", "🔮", "🌺"][i % 8]
            st.markdown(
                f'<div class="feature-item">{emoji} {sentence.strip()}.</div>',
                unsafe_allow_html=True,
            )

    with cols[1]:
        st.image(
            f"products/{chosen_product}.jpg",
            use_container_width=True,
            caption=f"✨ {chosen_product} ✨",
        )

    # Add final sentence as a closing highlight
    if last_sentence:
        st.markdown(
            f'<div class="closing-highlight sparkle">{translate("lucky.closing_highlight", sentence=last_sentence)}</div>',
            unsafe_allow_html=True,
        )

    # Add some extra visual flair
    st.markdown(
        """
    <div style="text-align: center; margin-top: 2rem; opacity: 0.7;">
        <span style="font-size: 1.5rem;">✨ 🌟 ✨ 🌟 ✨</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Footer with decorative elements
    st.markdown(
        """
    <div style="text-align: center; margin-top: 3rem; padding: 2rem; color: #666;">
        <p style="font-style: italic;">AI can make mistakes, please verify the information before making a purchase.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
