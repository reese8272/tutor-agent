from agents.state import TutorAgentState
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableConfig
from prompts.feedback_prompt import feedback_prompt
from langchain_core.runnables import RunnableLambda

from langgraph.graph import StateGraphNode

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", temperature=0)

parser = JsonOutputParser()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", feedback_prompt),
        ("human", "{question}"),
        ("user", "{user_answer}"),
    ]
)

chain = prompt | llm | parser

def generate_feedback(state: TutorAgentState) -> TutorAgentState:
    question = state.current_question.text
    user_answer = state.user_input

    try:
        result = chain.invoke({
            "question": question,
            "user_answer": user_answer
        }, config=RunnableConfig(tags=["feedback"]))

        state.last_feedback = result.get("feedback", "").strip()
        state.last_correct = result.get("correct", False)

    except Exception as e:
        state.last_feedback = f"[⚠️] Error generating feedback: {e}"
        state.last_correct = False

    return state

node = generate_feedback
