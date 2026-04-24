# simple_reviewer.py - With parsing
from langchain_groq import ChatGroq
import os
import re
from dotenv import load_dotenv

load_dotenv()
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

def review(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    print(f"📄 Reviewing: {file_path} ({len(code.splitlines())} lines)")
    
    prompt = f"""Review this Python code. Answer these questions:
        1. Does it PASS code review? (yes/no)
        2. Score out of 100?
        3. List any critical issues (syntax errors, security risks, broken imports)
        4. List any warnings (performance issues, potential bugs)

        Code:
        {code}

        Format your response as:
        PASS: yes/no
        SCORE: number
        CRITICAL_ISSUES: list
        WARNINGS: list"""
    
    response = llm.invoke(prompt)
    content = response.content
    
    # Parse the response
    print("\n" + "="*60)
    print("CODE REVIEW REPORT")
    print("="*60)
    print(content)
    
    # Extract key information
    pass_match = re.search(r'PASS:\s*(yes|no)', content, re.IGNORECASE)
    score_match = re.search(r'SCORE:\s*(\d+)', content, re.IGNORECASE)
    
    if pass_match:
        print(f"\n✓ Review Result: {'PASSED' if pass_match.group(1).lower() == 'yes' else 'FAILED'}")
    if score_match:
        print(f"✓ Score: {score_match.group(1)}/100")
    
    return content

# Run review
result = review("test.py")