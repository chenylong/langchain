from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

model_name ="llama3.1:latest"

# 初始化 Ollama 模型
llm = Ollama(base_url="http://localhost:11434", model=model_name)

# 创建提示模板
template = "回答以下问题：{question}"
prompt = PromptTemplate(template=template, input_variables=["question"])

# 创建 LLM 链
chain = LLMChain(llm=llm, prompt=prompt)

# 用户输入问题
question = input("请输入您的问题：")

# 生成答案
answer = chain.run(question)

# 显示答案
print(f"答案是：{answer}")