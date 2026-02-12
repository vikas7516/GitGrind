"""
GitGrind — Answer validation.
Normalizes user input and checks against accepted answers.
"""
import re
import functools


def normalize(text):
    """Normalize whitespace and casing for comparison."""
    text = text.strip().lower()
    text = re.sub(r'\s+', ' ', text)
    # Normalize quotes: treat single/double and smart quotes the same
    text = text.replace('\u201c', '"').replace('\u201d', '"')
    text = text.replace('\u2018', "'").replace('\u2019', "'")
    return text


def _strip_git_prefix(text):
    """Strip leading 'git ' prefix only (not all occurrences)."""
    if text.startswith("git "):
        return text[4:]
    return text

@functools.lru_cache(maxsize=256)
def _build_placeholder_regex(answer_norm):
    """Build a compiled regex that treats <placeholders> as non-space tokens."""
    tokens = answer_norm.split()
    regex_parts = []
    for token in tokens:
        if re.fullmatch(r"<[^>]+>", token):
            regex_parts.append(r"\S+")
        else:
            regex_parts.append(re.escape(token))
    pattern_str = r"^" + r"\s+".join(regex_parts) + r"$"
    return re.compile(pattern_str)


def check_answer(user_input, accepted_answers):
    """
    Check if user input matches any of the accepted answers.
    Returns (is_correct, matched_answer_or_None).
    """
    user_norm = normalize(user_input)
    user_variants = {user_norm, _strip_git_prefix(user_norm)}

    for answer in accepted_answers:
        answer_norm = normalize(answer)
        answer_variants = {answer_norm, _strip_git_prefix(answer_norm)}

        for user_variant in user_variants:
            # Exact match after normalization
            if user_variant in answer_variants:
                return True, answer

        # Placeholder-aware match (e.g., "git push <url>")
        for answer_variant in answer_variants:
            regex = _build_placeholder_regex(answer_variant)
            if regex.match(user_norm):
                return True, answer
            if regex.match(_strip_git_prefix(user_norm)):
                return True, answer

    return False, None


def check_fill_blank(user_input, accepted_answers):
    """
    For fill-in-the-blank exercises.
    The user types just the blank portion.
    """
    user_norm = normalize(user_input)

    for answer in accepted_answers:
        answer_norm = normalize(answer)
        if user_norm == answer_norm:
            return True, answer

    return False, None


def check_multi_choice(user_input, correct_letter):
    """
    For multiple choice questions.
    User types 'a', 'b', 'c', etc.
    """
    user_norm = normalize(user_input).strip().rstrip(')')
    correct_norm = normalize(correct_letter).strip().rstrip(')')

    return user_norm == correct_norm, correct_letter
