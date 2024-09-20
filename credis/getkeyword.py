#利用本地大模型lama3.12，对文本进行分词，并生成kg
# -*- coding: utf-8 -*-
from datetime import datetime
import os
import requests
import json
# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
#model = "qwen:14b-chat-v1.5-q4_0"
model = "llama3.1:latest"
def chat(messages):
    r = requests.post(
        "http://192.168.1.169:11434/api/chat",
        json={"model": model, "messages": messages, "stream": True},
    )

    r.raise_for_status()
    output = ""
    for line in r.iter_lines():
        body = json.loads(line)
        if "error" in body:
            raise Exception(body["error"])
        if body.get("done") is False:
            message = body.get("message", "")
            content = message.get("content", "")
            output += content
            # the response streams one token at a time, print that as we receive it
            #print(content, end="", flush=True)
        if body.get("done", False):
            message["content"] = output
            return output

def getkeywordbytext(text):
    prompt_str = f'''
我是行政执法人员，我正在对一些法律文本进行分析，需要你的帮助。我需要你从一段文本中提取其中主要违法行为、法对象的信息。并提炼其违法行为的关键字或短语列表。
以下是具体的要求：
1. 关键字应能够概括文本的主要内容和主题，但是像 行政主管部门、处罚、违法次数、罚款、罚款金额等非违法行为相关的内容不用展示。
2. 请提取文本中最重要的描述行政违法行为、违法对象的信息。
3. 保持关键字的多样性，确保它们涵盖文本的不同方面。
4. 关键字或短语可以是词语或短语。
5. 关键字或短语应该是文本中出现过的内容，不要臆造。
6. 只需给出具体的关键字或短语即可，其他无关内容不需要输出。输出前，请检查关键词个数是否在1到10之间，如果不在，则重新提取。
7. 输出格式为数组格式，形如：
</result>xxx1|xxx2|xxx3</result>
其他无关内容不要输出
给定的文本如下：
<content>{text}</content>
'''
    messages = [{"role": "user", "content": prompt_str}]

    return chat(messages)

if __name__ == "__main__":

    text = "餐厨垃圾产生单位自行就地处置餐厨垃圾未报送备案的应依据《浙江省餐厨垃圾管理办法》第三十一条“有下列行为之一的，由市容环卫行政主管部门责令限期改正；逾期不改正的，按以下规定处罚：违反本办法第九条第三款的规定，餐厨垃圾产生单位自行就地处置餐厨垃圾未报送备案的，处以1000元以上5000元以下罚款。”的规定予以处罚。"
    
    text2 = '''占用、挖掘城市道路设施不按规定设置交通安全护栏和标志的应根据《杭州市市政设施管理条例》第五十八条第二款“占用、挖掘城市道路设施、桥涵设施、城市河道设施不按规定设置交通安全护栏和标志，挖掘工程完成后不按规定回填夯实，或占用、挖掘结束后不及时清理现场、拆除临时设施的，由城市管理行政执法机关责令限期纠正，并可处五百元以上五千元以下罚款，造成他人伤害或损失的，应当赔偿损失”的规定予以行政处罚。
一年内首次违法且违法情节轻微，不按规定设置交通安全标志的施工现场面积在5㎡以下，当事人能按要求及时改正，且未影响道路通行安全，未造成损失的，不予行政处罚。二次以上违法的，处500元以上800元以下罚款。'''

    ss = getkeywordbytext(text2)
    print(ss)
        