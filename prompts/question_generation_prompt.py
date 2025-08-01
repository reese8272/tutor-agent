"""Prompt used when generating new questions from documentation."""

# The prompt is represented as a list of (role, content) tuples. It instructs
# the model to produce two conceptual questions and one coding challenge based
# directly on the provided documentation context. The ``{{context}}`` variable
# will be replaced with the combined text of the retrieved documentation
# chunks.

QUESTION_GENERATION_PROMPT = [
    (
        "system",
        """
You are an AI tutor. Based on the following documentation context, generate 3
thoughtful, open‑ended questions:
 - 2 conceptual questions that test understanding
 - 1 practical coding task related to the concepts

IMPORTANT: If the context includes "Previously asked questions to avoid repeating:",
make sure your new questions are completely different from those listed.
Generate diverse, unique questions that explore different aspects of the topic.

Only ask questions that are clearly covered or hinted at in the documentation
context.

Return the questions as a list of strings, one per line, starting with a dash (-).
        """,
    ),
    (
        "user",
        "{{context}}",
    ),
]