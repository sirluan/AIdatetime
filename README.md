# 基于AI的日期时间解析器
python 内置的datetime模块处理日期时间能力有限，借助AI工具可以更好处理它们

```python
from AIdatetime import chat_model, get_datetime
# 设置环境变量可以不添加api_key参数
os.environ["OPENAI_API_KEY"] = "your_api_key"

# 以通义千问为例
model_name = 'qwen-turbo'
base_url = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
chain = chat_model(model_name,base_url,api_key,templates)
print(get_datetime(chain, "2025年12月31日的11:59:00"))
```

也可以处理更多字符串
```python
get_datetime(chain, "25年12月31日的11:59:00") # 补充为2025-12-31 11:59:00
get_datetime(chain, "2025年11月最后一天") # 2025-11-30 00:00
get_datetime(chain, "11点钟") # 1901-01-01 11:00:00
```

还可以添加预设词
```python
template = '默认为2025年'
get_datetime(chain, "12月31日的11:59:00") # 2025-12-31 11:59:00
```

其中`get_datetime()`返回值为python的datetime库的datetime类型,可以使用year,month,day,hour,minite,second等方法
