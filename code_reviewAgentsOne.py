import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"

from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

GUIDELINES = """
        1. Proper indentation (4 spaces)
        2. Imports declared at top of file
        3. Uniform naming convention (snake_case for functions/variables, PascalCase for classes)
        4. No unused imports
        5. Docstrings for all functions and classes
        6. No hardcoded values (use constants or env variables)
        7. Proper error handling (try/except)
        8. No overly long functions (>50 lines)
        9. Consistent spacing between functions (2 blank lines)
        10. No commented out code
    """

def review_file(filepath):
    # Read file
    with open(filepath, "r", encoding='utf-8') as f:
        code = f.read()
    
    print(f"✅ File read: {len(code.splitlines())} lines")
    
    prompt = f"""You are a Python code reviewer. Review the following code against these guidelines:
        {GUIDELINES}

        Code:
        {code}

        Provide a detailed review with:
        1. Issues found (with line numbers)
        2. Severity (High/Medium/Low)
        3. Suggestion to fix"""

    response = llm.invoke(prompt)
    return response.content


if __name__ == "__main__":
    print(review_file("test.py"))