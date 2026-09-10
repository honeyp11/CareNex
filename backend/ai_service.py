# pyrefly: ignore [missing-import]
from google import genai
# pyrefly: ignore [missing-import]
from google.genai import types
from config.settings import SUPPORTED_MODELS

def get_system_instruction(user_stage: str, target_domain: str) -> str:
    """Generates dynamic CareNex system persona prompt tailored to user context."""
    return f"""
You are "CareNex", a world-class AI Career Counselor, Industry Mentor, and Strategic Advisor.
The user is: "{user_stage}" targeting: "{target_domain}".

Your Core Directives:
1. Provide structured, realistic, step-by-step career blueprints and actionable guidance.
2. Structure roadmaps with clear progressive milestones: Foundations → Practical Projects → Interview & Job Readiness.
3. Recommend top-tier, reputable free resources (official documentation, top GitHub roadmaps, industry certifications).
4. Emphasize actual industry standards, hiring demands, and portfolio proof.
5. If the user asks in Hindi or Hinglish, respond warmly in natural, fluent Hinglish. If in English, respond in crisp, professional English.
6. Use clean Markdown formatting: bullet points, bold keywords, comparison tables, and code snippets when appropriate.
7. Tone: Inspiring, approachable, friendly, and practical. Keep the user motivated and engaged.
"""

def stream_chat_response(prompt: str, message_history: list, user_stage: str, target_domain: str, model_choice: str, api_key: str):
    """
    Streams the assistant response from Gemini, automatically falling back to alternative
    models if the primary selected model encounters quota or availability issues.
    Yields (chunk_text, is_fallback_notice).
    """
    if not api_key:
        raise ValueError("Gemini API Key is not configured.")

    system_instruction = get_system_instruction(user_stage, target_domain)

    # Build concise recent history context
    history_context = ""
    for prev in message_history[-6:-1]:
        history_context += f"{prev['role'].capitalize()}: {prev['content']}\n"

    full_prompt = f"{history_context}\nUser: {prompt}\n(Provide structured, practical advice with markdown formatting)"

    # Primary model attempt
    try:
        client = genai.Client(api_key=api_key)
        chat = client.chats.create(
            model=model_choice,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
            )
        )
        for chunk in chat.send_message_stream(full_prompt):
            if chunk.text:
                yield chunk.text, False
        return

    except Exception as primary_err:
        print(f"[AI Service Warning] Model {model_choice} failed: {primary_err}. Attempting fallbacks...")

    # Fallback cascade
    fallback_models = [m for m in SUPPORTED_MODELS if m != model_choice]
    last_error = None

    for fb_model in fallback_models:
        try:
            yield f"🔄 *Optimizing response with {fb_model}...*\n\n", True
            client = genai.Client(api_key=api_key)
            chat = client.chats.create(
                model=fb_model,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7,
                )
            )
            for chunk in chat.send_message_stream(prompt):
                if chunk.text:
                    yield chunk.text, False
            return
        except Exception as fb_err:
            last_error = fb_err
            continue

    raise RuntimeError(f"All AI models failed. Last error: {last_error}")
