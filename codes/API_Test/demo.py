
from utils import client

completion = client.chat.completions.create(
  model="gpt-4o-mini", # this field is currently unused
  messages=[
    {"role": "user",
    "content": "你好"}
  ],
  temperature=0.7,
)
print(completion.choices[0].message.content)# 输出文案