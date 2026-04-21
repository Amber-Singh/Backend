from pydantic import BaseModel

class TestCase(BaseModel):
    test_id: str
    test_name: str
    category: str
    method: str
    endpoint: str
    expected_status: int
    request_body: dict = {}
    expected_response: dict = {}
    headers: dict = {}