# pyrefly: ignore [missing-import]
import streamlit as st
from frontend.styles import get_mascot_base64
from config.settings import resolve_api_key
from database.session_repo import (
    create_session,
    save_message,
    update_session_title
)
from backend.export_service import (
    export_session_as_pdf,
    export_session_as_text,
    export_session_as_markdown
)
from backend.ai_service import stream_chat_response

def render_chat_view(detected_key: str):
    """Renders the Dedicated Chat View (GammaBot / Personal AI Buddy Mockup Style)."""
    # Re-check key in case user entered it in session
    if not detected_key:
        detected_key = resolve_api_key()

    # 1. Chat App Header Bar
    ch_col1, ch_col2, ch_col3, ch_col4 = st.columns([0.20, 0.46, 0.16, 0.18])
    with ch_col1:
        if st.button("← Home", use_container_width=True):
            st.session_state.current_view = "home"
            st.rerun()

    with ch_col2:
        mascot_b64 = get_mascot_base64()
        mascot_thumb_html = f'<img src="data:image/jpeg;base64,{mascot_b64}" alt="bot">' if mascot_b64 else '🤖'
        st.markdown(f"""
        <div class="chat-header-bot">
            {mascot_thumb_html}
            <div>
                <h3>CareNex</h3>
                <p><span class="pulse-green"></span> Online • {st.session_state.model_choice}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with ch_col3:
        if st.button("➕ New", help="Start new conversation", use_container_width=True):
            new_sid = create_session(user_stage=st.session_state.user_stage, target_domain=st.session_state.target_domain)
            st.session_state.session_id = new_sid
            st.session_state.messages = []
            st.rerun()

    with ch_col4:
        with st.popover("📥 Export", use_container_width=True):
            if not st.session_state.messages:
                st.info("💡 **Consultation is Empty**\n\nAsk CareNex a question or pick a starter prompt below. Once you start chatting, you can export your complete consultation report here.")
            else:
                msg_count = len(st.session_state.messages)
                st.markdown(f"<p style='font-size: 0.85rem; font-weight: 700; color: #00d2b4; margin-bottom: 6px;'>Export Consultation ({msg_count} messages):</p>", unsafe_allow_html=True)
                
                # PDF Download
                pdf_bytes = export_session_as_pdf(
                    st.session_state.session_id,
                    user_stage=st.session_state.user_stage,
                    target_domain=st.session_state.target_domain,
                    messages=st.session_state.messages
                )
                st.download_button(
                    "📄 PDF Document (.pdf)",
                    data=pdf_bytes,
                    file_name=f"carenex_{st.session_state.session_id[:8]}.pdf",
                    mime="application/pdf",
                    key=f"chat_export_pdf_{msg_count}",
                    use_container_width=True
                )

                # Plain Text Download
                txt_data = export_session_as_text(
                    st.session_state.session_id,
                    user_stage=st.session_state.user_stage,
                    target_domain=st.session_state.target_domain,
                    messages=st.session_state.messages
                )
                st.download_button(
                    "📝 Plain Text (.txt)",
                    data=txt_data,
                    file_name=f"carenex_{st.session_state.session_id[:8]}.txt",
                    mime="text/plain",
                    key=f"chat_export_txt_{msg_count}",
                    use_container_width=True
                )

                # Markdown Download
                md_data = export_session_as_markdown(
                    st.session_state.session_id,
                    user_stage=st.session_state.user_stage,
                    target_domain=st.session_state.target_domain,
                    messages=st.session_state.messages
                )
                st.download_button(
                    "📑 Markdown (.md)",
                    data=md_data,
                    file_name=f"carenex_{st.session_state.session_id[:8]}.md",
                    mime="text/markdown",
                    key=f"chat_export_md_{msg_count}",
                    use_container_width=True
                )

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # Inline API Key Connection Card (Only shown if key is missing)
    if not detected_key:
        st.markdown("""
        <div style="background: rgba(15, 21, 35, 0.85); border: 1px solid rgba(0, 210, 180, 0.35); border-radius: 18px; padding: 18px 20px; margin: 10px 0 16px 0;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
                <span style="font-size: 1.4rem;">🔑</span>
                <h3 style="color: #ffffff; margin: 0; font-size: 1.05rem; font-family: 'Outfit', sans-serif;">Connect Gemini API Key</h3>
            </div>
            <p style="color: #94a3b8; font-size: 0.82rem; margin: 0 0 12px 0; line-height: 1.4;">
                To activate CareNex on this device, enter your Gemini API key below or configure <code>GEMINI_API_KEY</code> in Streamlit Secrets.
            </p>
        </div>
        """, unsafe_allow_html=True)

        c_k1, c_k2 = st.columns([0.72, 0.28])
        with c_k1:
            k_input = st.text_input("Gemini API Key:", type="password", placeholder="Paste API Key (AIzaSy...)", key="inline_chat_api_key", label_visibility="collapsed")
        with c_k2:
            if st.button("Connect ⚡", key="btn_connect_inline_key", use_container_width=True):
                if k_input and k_input.strip():
                    st.session_state.custom_api_key = k_input.strip()
                    st.rerun()
                else:
                    st.warning("Please paste a valid key.")

        st.markdown("<p style='font-size: 0.74rem; color: #64748b; margin-top: -6px; padding: 0 4px;'>Get a free key at <a href='https://aistudio.google.com/apikey' target='_blank' style='color: #00d2b4; text-decoration: none;'>Google AI Studio ↗</a>. Your key is stored in your browser session only.</p>", unsafe_allow_html=True)

    # 2. Render Interactive Empty Welcome Card (When No Messages)
    if not st.session_state.messages and not st.session_state.pending_prompt:
        st.markdown(f"""
        <div style="text-align: center; padding: 28px 20px 20px 20px; background: rgba(15, 21, 35, 0.7); border-radius: 20px; border: 1px solid rgba(0, 210, 180, 0.25); margin-bottom: 20px;">
            <div style="font-size: 2.8rem; margin-bottom: 8px;">⚡</div>
            <h3 style="color: #ffffff; margin: 0 0 6px 0; font-family: 'Outfit', sans-serif;">How can CareNex guide your career today?</h3>
            <p style="color: #94a3b8; font-size: 0.88rem; max-width: 480px; margin: 0 auto 16px auto;">
                Select a quick prompt below or type any question to begin personalized mentorship in <strong>{st.session_state.target_domain}</strong>.
            </p>
        </div>
        """, unsafe_allow_html=True)

        c_s1, c_s2 = st.columns(2)
        with c_s1:
            if st.button("🗺️ Build My 6-Month Roadmap", key="chat_starter_roadmap", use_container_width=True):
                st.session_state.pending_prompt = f"Give me a step-by-step 6-month roadmap to become job-ready in {st.session_state.target_domain} as a {st.session_state.user_stage}."
                st.rerun()
            if st.button("💼 Best Portfolio Projects", key="chat_starter_projects", use_container_width=True):
                st.session_state.pending_prompt = f"What are 3 high-impact portfolio projects that recruiters love for {st.session_state.target_domain}?"
                st.rerun()
        with c_s2:
            if st.button("⚡ Top Skills to Learn First", key="chat_starter_skills", use_container_width=True):
                st.session_state.pending_prompt = f"What are the top 5 highest-paying and most demanded skills in {st.session_state.target_domain} right now?"
                st.rerun()
            if st.button("🎤 Practice Interview Q&A", key="chat_starter_interview", use_container_width=True):
                st.session_state.pending_prompt = f"Ask me the #1 most common interview question for {st.session_state.target_domain} and guide me on how to answer it."
                st.rerun()

    # 3. Render Message History
    for msg in st.session_state.messages:
        is_user = (msg["role"] == "user")
        with st.chat_message(msg["role"], avatar="🧑‍💻" if is_user else "⚡"):
            st.markdown(msg["content"])

    # 4. Interactive Quick Follow-up Chips (When Conversation is Active)
    if st.session_state.messages:
        st.markdown("<div style='margin-top: 14px; margin-bottom: 6px;'><span style='font-size: 0.76rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em;'>Quick Follow-Ups (Tap to Ask):</span></div>", unsafe_allow_html=True)
        fc1, fc2, fc3, fc4 = st.columns(4)
        with fc1:
            if st.button("📌 Next Steps", key="chip_next", use_container_width=True):
                st.session_state.pending_prompt = "What are my immediate next 3 action steps based on your advice above?"
                st.rerun()
        with fc2:
            if st.button("💼 Project Ideas", key="chip_proj", use_container_width=True):
                st.session_state.pending_prompt = "Give me 2 real-world hands-on project ideas to practice these skills."
                st.rerun()
        with fc3:
            if st.button("📄 Resume Tips", key="chip_res", use_container_width=True):
                st.session_state.pending_prompt = "How should I describe these skills and projects on my resume to pass ATS scanners?"
                st.rerun()
        with fc4:
            if st.button("🎤 Interview Prep", key="chip_int", use_container_width=True):
                st.session_state.pending_prompt = "What questions would an interviewer ask about this topic, and what is the ideal answer?"
                st.rerun()

    # 5. Handle Input (from chat_input or pending starter action)
    prompt_to_send = None
    if st.session_state.pending_prompt:
        prompt_to_send = st.session_state.pending_prompt
        st.session_state.pending_prompt = None
    elif user_input := st.chat_input("Ask CareNex anything about your career roadmap, skills, resume..."):
        prompt_to_send = user_input

    if prompt_to_send:
        # Re-resolve key
        if not detected_key:
            detected_key = resolve_api_key()

        if not detected_key:
            st.warning("🔑 Please enter your Gemini API Key above to begin chatting.")
            st.stop()

        # Save user turn to state and MongoDB
        st.session_state.messages.append({"role": "user", "content": prompt_to_send})
        save_message(st.session_state.session_id, "user", prompt_to_send)

        if len(st.session_state.messages) == 1:
            update_session_title(st.session_state.session_id, prompt_to_send)

        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt_to_send)

        # Stream Assistant turn
        with st.chat_message("assistant", avatar="⚡"):
            response_placeholder = st.empty()
            response_placeholder.markdown("""
            <div style="display: flex; align-items: center; gap: 8px; color: #00d2b4; font-size: 0.88rem;">
                <span class="pulse-green"></span> <em>CareNex is thinking & preparing your guidance...</em>
            </div>
            """, unsafe_allow_html=True)

            try:
                full_response = ""
                for chunk, is_notice in stream_chat_response(
                    prompt=prompt_to_send,
                    message_history=st.session_state.messages,
                    user_stage=st.session_state.user_stage,
                    target_domain=st.session_state.target_domain,
                    model_choice=st.session_state.model_choice,
                    api_key=detected_key
                ):
                    full_response += chunk
                    response_placeholder.markdown(full_response + "▌")

                response_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                save_message(st.session_state.session_id, "assistant", full_response)
                st.rerun()

            except Exception as err:
                response_placeholder.error(f"Error generating response: {str(err)}")
