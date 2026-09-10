# pyrefly: ignore [missing-import]
import streamlit as st
from .header import render_top_header
from frontend.styles import get_mascot_base64
from database.session_repo import list_sessions, get_session_messages
from backend.export_service import (
    export_session_as_pdf,
    export_session_as_text,
    export_session_as_markdown
)

def render_home_view():
    """Renders the Home View (Mockup GammaBot / Personal AI Buddy Style)."""
    # 1. Top Header
    render_top_header()

    # 2. Hero Mascot Card
    mascot_b64 = get_mascot_base64()
    mascot_img_html = f'<img src="data:image/jpeg;base64,{mascot_b64}" alt="CareNex">' if mascot_b64 else '<div style="font-size: 5rem;">🤖</div>'
    
    st.markdown(f"""
    <div class="hero-card">
        <div class="hero-text-side">
            <div class="hero-tag">⚡ CareNex AI Mentor</div>
            <h1 class="hero-headline">Ask Your Career Question</h1>
            <p class="hero-subline">Meet CareNex! Your personalized AI counselor for customized roadmaps, skill audits, and interview preparation.</p>
        </div>
        <div class="hero-img-side">
            {mascot_img_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Hero CTA Button to Start Chatting
    c_btn1, c_btn2, c_btn3 = st.columns([0.05, 0.9, 0.05])
    with c_btn2:
        st.markdown('<div class="cta-neon-btn">', unsafe_allow_html=True)
        if st.button("💬 Chat with CareNex Now", use_container_width=True):
            st.session_state.current_view = "chat"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # 3. Quick Action Grid (2x2 matching mockup style)
    st.markdown("""
    <div class="section-header">
        <h3 class="section-title">⚡ Quick Starters</h3>
    </div>
    """, unsafe_allow_html=True)

    q1, q2 = st.columns(2)
    with q1:
        st.markdown("""
        <div class="action-card">
            <div class="action-card-header">
                <div class="action-card-icon">🗺️</div>
                <div class="action-card-arrow">↗</div>
            </div>
            <div>
                <p class="action-card-title">Career Roadmap</p>
                <p class="action-card-sub">0 to job-ready milestone plan</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Generate Roadmap ↗", key="home_btn_roadmap", use_container_width=True):
            st.session_state.pending_prompt = f"Please give me a realistic, step-by-step 6-month roadmap to become job-ready in {st.session_state.target_domain}. I am a {st.session_state.user_stage}."
            st.session_state.current_view = "chat"
            st.rerun()

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="action-card">
            <div class="action-card-header">
                <div class="action-card-icon">🎤</div>
                <div class="action-card-arrow">↗</div>
            </div>
            <div>
                <p class="action-card-title">Mock Interview</p>
                <p class="action-card-sub">Real technical & HR screening</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Practice Interview ↗", key="home_btn_interview", use_container_width=True):
            st.session_state.pending_prompt = f"Act as a hiring manager for {st.session_state.target_domain}. Ask me the #1 most common interview question and give me feedback on how to structure a winning answer."
            st.session_state.current_view = "chat"
            st.rerun()

    with q2:
        st.markdown("""
        <div class="action-card">
            <div class="action-card-header">
                <div class="action-card-icon">⚡</div>
                <div class="action-card-arrow">↗</div>
            </div>
            <div>
                <p class="action-card-title">Skills & Certs</p>
                <p class="action-card-sub">Highest ROI industry skills</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Analyze Skills ↗", key="home_btn_skills", use_container_width=True):
            st.session_state.pending_prompt = f"What are the top 5 highest-paying and most demanded technical skills in {st.session_state.target_domain} for 2026? Include recognized certifications."
            st.session_state.current_view = "chat"
            st.rerun()

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="action-card">
            <div class="action-card-header">
                <div class="action-card-icon">💼</div>
                <div class="action-card-arrow">↗</div>
            </div>
            <div>
                <p class="action-card-title">Project Ideas</p>
                <p class="action-card-sub">Recruiter-ready portfolio work</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Suggest Projects ↗", key="home_btn_projects", use_container_width=True):
            st.session_state.pending_prompt = f"What are 3 high-impact, unique portfolio projects for {st.session_state.target_domain} that will genuinely impress recruiters and pass ATS scanners?"
            st.session_state.current_view = "chat"
            st.rerun()

    # 4. Trending Topics Tags
    st.markdown("""
    <div class="section-header">
        <h3 class="section-title">🔥 Trending Career Paths</h3>
    </div>
    """, unsafe_allow_html=True)

    t_cols = st.columns(4)
    topics = [
        ("🤖 AI Engineer", "Artificial Intelligence & Machine Learning"),
        ("🌐 Full Stack", "Software Development & Web Tech"),
        ("☁️ Cloud DevOps", "Cloud Computing & DevOps"),
        ("🛡️ Cybersecurity", "Cybersecurity & Ethical Hacking")
    ]
    for i, (tag_label, domain_name) in enumerate(topics):
        with t_cols[i]:
            if st.button(tag_label, key=f"topic_{i}", use_container_width=True):
                st.session_state.target_domain = domain_name
                st.session_state.pending_prompt = f"Give me an introductory roadmap and essential starter guide for becoming a {domain_name}."
                st.session_state.current_view = "chat"
                st.rerun()

    # 5. History Consultations (Loaded from MongoDB)
    st.markdown("""
    <div class="section-header">
        <h3 class="section-title">🕒 Recent Consultations</h3>
        <span class="section-link">Stored in MongoDB</span>
    </div>
    """, unsafe_allow_html=True)

    recent_sessions = list_sessions(limit=5)
    if recent_sessions:
        for s in recent_sessions:
            sid = s["session_id"]
            title = s.get("title") or "Career Consultation"
            count = s.get("message_count", 0)
            
            c_hist_left, c_hist_btn, c_hist_dl = st.columns([0.68, 0.16, 0.16])
            with c_hist_left:
                st.markdown(f"""
                <div class="history-card">
                    <div class="history-left">
                        <div class="history-icon-bubble">💬</div>
                        <div class="history-info">
                            <h4>{title}</h4>
                            <p>{count} messages • {s.get('target_domain', 'General')}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with c_hist_btn:
                if st.button("Open >", key=f"hist_open_{sid}", use_container_width=True):
                    st.session_state.session_id = sid
                    st.session_state.messages = get_session_messages(sid)
                    st.session_state.current_view = "chat"
                    st.rerun()
            with c_hist_dl:
                with st.popover("📥", help="Export this chat in PDF, Text, or Markdown"):
                    st.caption(f"Export: {title[:20]}...")
                    try:
                        hist_pdf = export_session_as_pdf(sid, s.get("user_stage", ""), s.get("target_domain", "General"))
                        st.download_button("📄 PDF (.pdf)", data=hist_pdf, file_name=f"carenex_{sid[:8]}.pdf", mime="application/pdf", key=f"dl_pdf_{sid}_{count}", use_container_width=True)
                    except Exception as err:
                        st.caption(f"PDF unavailable: {err}")
                    try:
                        hist_txt = export_session_as_text(sid, s.get("user_stage", ""), s.get("target_domain", "General"))
                        st.download_button("📝 Text (.txt)", data=hist_txt, file_name=f"carenex_{sid[:8]}.txt", mime="text/plain", key=f"dl_txt_{sid}_{count}", use_container_width=True)
                    except Exception as err:
                        st.caption(f"Text unavailable: {err}")
                    try:
                        hist_md = export_session_as_markdown(sid, s.get("user_stage", ""), s.get("target_domain", "General"))
                        st.download_button("📑 Markdown (.md)", data=hist_md, file_name=f"carenex_{sid[:8]}.md", mime="text/markdown", key=f"dl_md_{sid}_{count}", use_container_width=True)
                    except Exception as err:
                        st.caption(f"Markdown unavailable: {err}")
    else:
        st.caption("No past consultations found yet. Start your first session above!")

    # Navigation toggles
    st.markdown("---")
    nav_c1, nav_c2, nav_c3 = st.columns(3)
    with nav_c1:
        st.button("🏠 Home (Active)", disabled=True, use_container_width=True)
    with nav_c2:
        if st.button("💬 Go to Chat", use_container_width=True):
            st.session_state.current_view = "chat"
            st.rerun()
    with nav_c3:
        if st.button("⚙️ Settings / Profile", use_container_width=True):
            st.session_state.current_view = "settings"
            st.rerun()
