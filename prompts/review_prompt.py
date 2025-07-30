### FILE: review_prompt.py
REVIEW_PROMPT = [
    (
        "system",
        """
The user has previously answered the following questions:

{{seen_questions}}

Based on this, generate:
- One conceptual follow-up question
- One new variation of a previous coding challenge

These should reinforce and expand the learner’s understanding.
        """
    ),
]