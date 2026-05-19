import os
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.tools import tool
from langchain_classic.agents import AgentExecutor, create_react_agent
from dotenv import load_dotenv
from prompt import SYSTEM_PROMPT
from tools import TOOLS

load_dotenv()
if "GOOGLE_API_KEY" not in os.environ:
    raise ValueError("GOOGLE_API_KEY environment variable not set. Please set it in your .env file.")

llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite",temperature=0)
agent = create_react_agent(llm,TOOLS, SYSTEM_PROMPT)
agent_executor = AgentExecutor(agent=agent,tools=TOOLS,verbose=True, handle_parsing_errors=True,max_iterations=8)

def parse_action(text: str):
    """Extract tool name and input from 'Action: tool[input]' lines."""
    match =re.search(r"Action:\s*(\w+)\[([^\]]*)\]", text)
    if match:
        return match.group(1), match.group(2).strip()
    return None, None

def run_agent(user_question: str, max_steps:int = 8)-> str:
    """Run the ReAct loop until a Final answer is produced or max_steps hit."""
    try:
        # Simply hand over the question to the executor
        response = agent_executor.invoke({"input": user_question})
        return response["output"]
    except Exception as e:
        return f"An error occurred: {e}"

# Entry point
if __name__ == "__main__":
    print("Web Search Agent (ReAct). Type 'quit' to exit.\n")
    while True:
        q = input("You: ").strip()
        if q.lower() in ("quit", "exit"):
            break
        answer = run_agent(q)
        print(f"\nFinal Answer: {answer}\n")