import streamlit as st
import random
from products.qa_data import questions as qa_collection
from scentmatch.graph import graph
from scentmatch.configuration import Configuration

# Load CSS from external file
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css('pages/styles.css')

if "result" not in st.session_state:
    if "selected_questions" not in st.session_state:
        st.session_state.selected_questions = random.sample(list(qa_collection.keys()), 3)

    questions = st.session_state.selected_questions
    answers = [qa_collection[question] for question in questions]

    # Enhanced title with decorative elements
    st.markdown('<h1 class="main-title sparkle">🌟 Legendary Scent Match 🌟</h1>', unsafe_allow_html=True)

    st.markdown("""
    <div class="subtitle">
        Discover your perfect fragrance through our personalized scent journey ✨
    </div>
    """, unsafe_allow_html=True)

    # Feature badges
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <span class="feature-badge">🎯 Personalized</span>
        <span class="feature-badge">🌸 Premium Scents</span>
        <span class="feature-badge">✨ AI-Powered</span>
        <span class="feature-badge">💫 Instant Results</span>
    </div>
    """, unsafe_allow_html=True)

    # Decorative divider
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Questions container
    # st.markdown('<div class="question-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <h2 style="text-align: center; color: #2d3748; margin-bottom: 2rem; font-size: 2rem;">
        🌺 Tell Us About Your Preferences 🌺
    </h2>
    """, unsafe_allow_html=True)

    user_responses = {}

    for i, (question, answer) in enumerate(zip(questions, answers), 1):
        # st.markdown(f'<div class="question-item">', unsafe_allow_html=True)
        st.markdown(f'<div class="question-title">Question {i}: {question}</div>', unsafe_allow_html=True)
        user_responses[question] = st.radio(
            f"Select your answer for question {i}:", 
            answer, 
            index=None,
            key=f"question_{i}",
            label_visibility="hidden"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Progress indicator
    user_answers = [answer for _, answer in user_responses.items() if answer is not None]
    progress = len(user_answers) / len(questions) * 100
    
    st.markdown(f"""
    <div class="progress-indicator">
        Progress: {len(user_answers)}/{len(questions)} questions answered ({progress:.0f}%)
        <div style="background: rgba(102, 126, 234, 0.3); height: 8px; border-radius: 4px; margin-top: 0.5rem;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); height: 100%; width: {progress}%; border-radius: 4px; transition: width 0.3s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Enhanced button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🌟 Find Your Perfect Scent! 🌟", key="find_scent_button"):
            # check if user has answered all questions
            if len(user_answers) == len(questions):
                st.markdown("""
                <div style="text-align: center; font-size: 1.5rem; color: #667eea; margin: 2rem 0;">
                    ✨ Analyzing your preferences... ✨
                </div>
                """, unsafe_allow_html=True)
                
                with st.spinner("🔮 Creating your personalized scent profile..."):
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
                st.error("💫 Please answer all questions to unlock your perfect scent match!")

    # Footer with decorative elements
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 2rem; color: #666;">
        <p style="font-style: italic;">✨ Your perfect scent is just a few clicks away ✨</p>
    </div>
    """, unsafe_allow_html=True)

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
        st.image(f"products/{chosen_product}.jpg", use_container_width=True, caption=f"✨ {chosen_product} ✨")

    # Add final sentence as a closing highlight
    if last_sentence:
        st.markdown(f'<div class="closing-highlight sparkle">🌸 {last_sentence} 🌸</div>', unsafe_allow_html=True)

    # Add some extra visual flair
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem; opacity: 0.7;">
        <span style="font-size: 1.5rem;">✨ 🌟 ✨ 🌟 ✨</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer with decorative elements
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 2rem; color: #666;">
        <p style="font-style: italic;">AI can make mistakes, please verify the information before making a purchase.</p>
    </div>
    """, unsafe_allow_html=True)