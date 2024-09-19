from langchain_community.llms import Tongyi
from langchain_core.prompts import PromptTemplate
import os 
from langchain_core.prompts import PromptTemplate
llm = Tongyi()

template = """Question: {question}
Answer: Let's think step by step."""
prompt = PromptTemplate.from_template(template)
chain = prompt | llm
question = "推荐一下主流的国内大模型?"
result_content = chain.invoke({"question": question})
print(result_content)