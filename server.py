from mcp.server.fastmcp import FastMCP
import httpx

# Your FastAPI app runs on this URL
API_BASE = "http://localhost:8000"

# Create the MCP server
mcp = FastMCP("Test Cases Server")

# --- TOOL: callable action (also fetches all tests) ---
@mcp.tool()
def list_all_tests() -> str:
    """Fetch and return all test cases."""
    response = httpx.get(f"{API_BASE}/tests/all")
    return response.text


 
# --- 2. GET TEST BY ID ---
@mcp.tool()
def get_test_by_id(test_id: str) -> str:
    """Fetch a single test case by its ID (e.g. C_002)."""
    response = httpx.get(f"{API_BASE}/tests/{test_id}")
    return response.text
 
 
# --- 3. SEARCH TESTS ---
@mcp.tool()
def search_tests(query: str) -> str:
    """Search test cases by keyword (e.g. 'login', 'order')."""
    response = httpx.get(f"{API_BASE}/tests/search/{query}")
    return response.text
 
 
# --- 4. GET TESTS BY CATEGORY ---
@mcp.tool()
def get_tests_by_category(category: str) -> str:
    """Get all tests in a category (e.g. 'Happy Path', 'Negative Path', 'Validation Error')."""
    response = httpx.get(f"{API_BASE}/tests/category/{category}")
    return response.text
 
 
# --- 5. DELETE TEST ---
@mcp.tool()
def delete_test(test_id: str) -> str:
    """Delete a test case by its ID (e.g. C_002)."""
    response = httpx.delete(f"{API_BASE}/tests/{test_id}")
    return response.text
 
 

# Run the server
if __name__ == "__main__":
    mcp.run()
    
#npx @modelcontextprotocol/inspector python server.py