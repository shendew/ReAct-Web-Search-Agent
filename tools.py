from ddgs import DDGS
from langchain_core.tools import tool  # Import the tool decorator

@tool 
def web_search(query:str)->str:
    """Search the web and return top 5 results as formatted text"""
    # Clean up the query from any accidental leftover brackets or quotes
    clean_query = query.strip(" '\" ")
    with DDGS() as ddgs:
        results = list(ddgs.text(clean_query, max_results=5))
    if not results:
        return "No results found."
    lines=[]
    for r in results:
        lines.append(f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}\n")
    return "\n".join(lines)

@tool 
def calculator(expression:str )->str:
    """Safely evaluate a math expression and return the result."""
    try:
        # 1. Strip external quotes and spaces
        clean_expression = expression.strip(" '\"")
        # 2. Normalize all internal whitespace (converts hidden \xa0, tabs, or multiple spaces into a single standard space)
        clean_expression = " ".join(clean_expression.split())

        #Only allow safe math -no exec od arbitary code
        allowed = set("0123456789+-*/().,% ")
        if not all( c in allowed for c in clean_expression):
            return "Error: only basic math operators allowed"
        result = eval(clean_expression,{"__builtins__":{}})
        return str(result)
    except Exception as e:
        return f"Error: {e}"
    
@tool
def get_current_date(_:str="")->str:
    """Return todays date."""
    from datetime import date
    return date.today().isoformat()

# Registry - the agent picks tools from the dict

TOOLS = [web_search,calculator,get_current_date]

# TOOLS = {
#     "web_search": web_search,
#     "calculator": calculator,
#     "get_current_date": get_current_date
# }
TOOL_DESCRIPTIONS = """
- web_search[query]: Search the web. Use for current events, facts, prices, news. Example: web_search[latest python release]
- calculator[expression]: Evaluate math. Example: calculator[150*1.08]
- get_current_date[]: Get todays date. Example: get_current_date[]
""".strip()