'''
output format
'''
from langchain_core.pydantic_v1 import BaseModel, Field

class Rule_schema(BaseModel):
    '''Quy tắc được viết theo mẫu logic như: <and>, <then>, <eor>'''
    type: str = Field(description="đầu ra là tập hợp các quy tắc logic")
