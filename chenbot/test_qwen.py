from langchain_community.llms import Tongyi
from langchain_core.prompts import PromptTemplate
import os 
from langchain_core.prompts import PromptTemplate
llm = Tongyi()


prompt_exp ='''参考样例：
<exp>
案情描述：2024年08月21日，我局在对当事人检查中发现2024年8月21日，余杭区市场监督管理局执法人员现场检查杭州余杭涛哥卤味店，发现从业人员廖艳珍未办理有效健康证明从事餐饮服务。
处理流程：
（1）获取违法行为信息
结果：从业人员廖艳珍未办理有效健康证明从事餐饮服务。
（2）提取完整的违法行为描述
结果：未办理有效健康证明从事餐饮服务
（3）关键词、组提取
结果：未办理、健康证明、从事餐饮服务
 （4）输出最终的关键词、组信息
</exp>'''

case_desc = "2024年9月12日14时当事人张来，在台州市椒江区白云街道1223号，白云广场西侧户外售卖衣物，但未办理相关营业执照。"

question = "请你将客户提供的案情描述中的违法行为进行总结和提炼，形成关键词、组返回。"


template = f"""问题: {question}。
案情描述：{case_desc}。
Answer: Let's think step by step.
你可以参考下面的样例，进行仔细分析
参考样例：
<exp>
案情描述：2024年08月21日，我局在对当事人检查中发现2024年8月21日，余杭区市场监督管理局执法人员现场检查杭州余杭涛哥卤味店，发现从业人员廖艳珍未办理有效健康证明从事餐饮服务。
处理流程：
（1）获取违法行为信息
结果：从业人员廖艳珍未办理有效健康证明从事餐饮服务。
（2）提取完整的违法行为描述
结果：未办理有效健康证明从事餐饮服务
（3）关键词、组提取
结果：未办理、健康证明、从事餐饮服务
 （4）输出最终的关键词、组信息
</exp>
注意：
最终只需输出具体的关键词、组的结果即可，其他无关内容不要输出
不要臆造，不要联网
"""
prompt = PromptTemplate.from_template(template)

chain = prompt | llm

print(prompt)
result_content = chain.invoke({"问题": question})

print(result_content)

# 根据反馈的关键词组，检索向量数据库 reids ，返回相似度最高的结果