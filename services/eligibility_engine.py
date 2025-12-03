from services.karnataka_board_service import get_board_overview

def _has_required_subjects(user_subjects, required_subjects):
    user_set = set([s.strip().title() for s in user_subjects])
    for req in required_subjects:
        if req not in user_set:
            return False, req
    return True, None

def check_kcet(subjects, percentage, years_in_karnataka=0, category="general"):
    """
    subjects: list of subject names e.g. ['Physics','Mathematics','Chemistry']
    percentage: float (0-100)
    years_in_karnataka: int
    category: 'general' or reserved categories
    Returns: (bool, message)
    """
    data = get_board_overview("kcet")
    if not data:
        return False, "KCET rules not available."

    rules = data["eligibility"]
    req_subjects = rules["required_subjects"]
    opt_subjects = rules["optional_subjects"]
    min_gen = rules["min_percentage_general"]
    min_res = rules["min_percentage_reserved"]
    min_years = rules.get("min_years_in_karnataka", 0)

    ok, missing = _has_required_subjects(subjects, req_subjects)
    if not ok:
        return False, f"Missing required subject: {missing}. KCET requires {', '.join(req_subjects)}."

    # optional check - at least one optional subject must be present
    user_set = set([s.strip().title() for s in subjects])
    if not any(opt in user_set for opt in opt_subjects):
        return False, f"KCET requires at least one optional subject among: {', '.join(opt_subjects)}."

    if category.lower() == "general":
        if percentage < min_gen:
            return False, f"Your percentage {percentage}% is less than the required {min_gen}% for general category."
    else:
        if percentage < min_res:
            return False, f"Your percentage {percentage}% is less than the required {min_res}% for reserved categories."

    if years_in_karnataka < min_years:
        return False, f"KCET domicile requirement: at least {min_years} years of study in Karnataka; you have {years_in_karnataka}."

    return True, "You meet the **basic** KCET eligibility criteria. (Check the official KEA brochure for category-specific clauses.)"

def check_comedk(subjects, percentage, category="general"):
    """
    COMED-K basic checks.
    """
    data = get_board_overview("comedk")
    if not data:
        return False, "COMED-K rules not available."

    rules = data["eligibility"]
    req_subjects = rules["required_subjects"]
    min_gen = rules["min_percentage_general"]
    min_kar = rules.get("min_percentage_karnataka_reserved", min_gen)

    ok, missing = _has_required_subjects(subjects, req_subjects)
    if not ok:
        return False, f"Missing required subject: {missing}. COMED-K requires {', '.join(req_subjects)}."

    if category.lower() == "general":
        if percentage < min_gen:
            return False, f"Your percentage {percentage}% is less than the required {min_gen}% for general category."
    else:
        if percentage < min_kar:
            return False, f"Your percentage {percentage}% is less than the required {min_kar}% for Karnataka reserved category."

    return True, "You meet the **basic** COMED-K UGET eligibility criteria. (Consult official COMED-K brochure for details.)"
