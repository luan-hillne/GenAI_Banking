'''
output format
'''
from langchain_core.pydantic_v1 import BaseModel, Field

class Rule_schema(BaseModel):
    '''logical expressions to represent the paragraph such as: <and>, <then>, <eor>'''
    type: str = Field(description="The method used is to combine logical expressions to represent the paragraph such as: <and>, <then>, <eor>")