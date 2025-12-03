from services.gemini_service import ask_gemini
from services.karnataka_board_service import get_kcet_info, get_comedk_info
from services.eligibility_engine import check_kcet, check_comedk

def handle_message(user_message, session_data=None):
    """
    session_data: optional dict for conversation/session context (not required)
    Returns: reply string and a dict 'meta' that may instruct the frontend
            (e.g., show eligibility form).
    """
    meta = {}
    text = user_message.strip().lower()

    # Intent detection: simple keywords — replace with real NLU if needed
    if "kcet" in text and ("eligib" in text or "am i" in text or "can i" in text):
        meta["show_form"] = "kcet"
        return "To check KCET eligibility u need: subjects (comma-separated), percentage, years studied in Karnataka, category (optional). Example: subjects: Physics, Mathematics, Chemistry; percentage: 85; years: 8; category: general", meta

    if "comed" in text and ("eligib" in text or "am i" in text or "can i" in text):
        meta["show_form"] = "comedk"
        return "To check COMED-K eligibility U need: subjects (comma-separated), percentage, category (optional). Example: subjects: Physics, Mathematics, Chemistry; percentage: 85; category: general", meta

    if "kcet info" in text or ("kcet" in text and "info" in text) or ("kcet" in text and "date" in text):
        data = get_kcet_info()
        if not data:
            return "KCET info is not available right now. Try later.", meta
        info = data.get("info", {})
        return f"KCET — official: {data.get('official')}\nExam window: {info.get('exam_window')}\nNotes: {data.get('eligibility', {}).get('notes')}", meta

    if "comedk info" in text or ("comedk" in text and "info" in text) or ("comedk" in text and "date" in text):
        data = get_comedk_info()
        if not data:
            return "COMED-K info is not available right now. Try later.", meta
        info = data.get("info", {})
        return f"COMED-K — official: {data.get('official')}\nExam window: {info.get('exam_window')}\nNotes: {data.get('eligibility', {}).get('notes')}", meta

    # If user provided a structured eligibility payload (we expect format: subjects: ...; percentage: ...; years: ...; category: ...)
    if "subjects:" in text and "percentage:" in text:
        # crude parsing but robust enough for demo. Expect semicolon-separated fields.
        try:
            parts = [p.strip() for p in user_message.split(";") if p.strip()]
            data = {}
            for p in parts:
                if ":" in p:
                    k, v = p.split(":", 1)
                    data[k.strip().lower()] = v.strip()
            subjects = [s.strip().title() for s in data.get("subjects", "").split(",") if s.strip()]
            percentage = float(data.get("percentage", "0").strip())
            years = int(data.get("years", "0").strip()) if "years" in data else 0
            category = data.get("category", "general").strip().lower()

            # Run both checks and return results
            k_ok, k_msg = check_kcet(subjects, percentage, years, category)
            c_ok, c_msg = check_comedk(subjects, percentage, category)
          
        except Exception as e:
            return "I couldn't parse your structured input. Please provide: subjects: Physics, Mathematics, Chemistry; percentage: 85; years: 8; category: general", meta

    # Fallback to Gemini for general admission Q&A
    prompt = f"You are an admissions assistant for an engineering college in Karnataka. Answer concisely.\nUser: {user_message}\nAssistant:"
    gemini_reply = ask_gemini(prompt)
    if not gemini_reply:
        return "Sorry — the AI helper is temporarily unavailable. Please try again later or ask eligibility-specific questions.", meta
    return gemini_reply, meta
