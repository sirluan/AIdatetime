import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from datetime import datetime
from typing import Optional

def chat_model(model_name: str, base_url: str, api_key: Optional[str] = None, template: str = ""):
    default_template = """
    你是日期解析工具，请根据用户输入的日期，返回日期信息。
    输入信息为：{input}
    使用工具date_parser或time_parser来解析日期。
    工具date_parser的参数格式为：YYYY-MM-DD HH:MM:SS，请将输入信息转换为该格式，如果输入缺少部分，请补全。
    如果没有年月日的信息就使用工具time_parser，参数格式为：HH:MM:SS，请将输入信息转换为该格式，如果缺少部分，请补全。
    如果无法转换，请返回None。
    """
    prompt = ChatPromptTemplate.from_template(default_template+template)
    if api_key is None:
        api_key = os.environ["OPENAI_API_KEY"]
    model = ChatOpenAI(
        model=model_name,
        base_url=base_url,
        api_key=api_key
    )
    tools = [date_parser, time_parser]
    model_with_tools = model.bind_tools(tools)
    chain = prompt | model_with_tools
    return chain

@tool
def date_parser(date: str):
    """
    日期解析工具，解析年月日时分秒

    参数：
    - date: 日期字符串，格式为YYYY-MM-DD HH:MM:SS

    返回：
    - 日期信息，包括年、月、日、时、分、秒
    """
    date_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    return date_obj

@tool
def time_parser(time: str):
    """
    时间解析工具，解析时分秒
    
    参数：
    - time: 时间字符串，格式为HH:MM:SS

    返回：
    - 时间信息，包括时、分、秒
    """
    time_obj = datetime.strptime(time, '%H:%M:%S')
    return time_obj

def call_tools(model_output, tools):
    tools_map = {tool.name.lower(): tool for tool in tools}
    tools_reponse = {}
    for tool in model_output.tool_calls:
        tool_name = tool['name']
        tool_args = tool['args']
        tool_instance = tools_map[tool_name]
        tool_response = tool_instance.invoke(*tool_args.values())
        tools_reponse[tool_name] = tool_response
    if 'date_parser' not in tools_reponse and 'time_parser' not in tools_reponse: raise ValueError("无法解析日期")
    return tools_reponse

def get_datetime(chain, date_str):
    model_output = chain.invoke({"input": date_str})
    date_obj = call_tools(model_output, [date_parser, time_parser])
    return date_obj['date_parser'] if 'date_parser' in date_obj else date_obj['time_parser']
