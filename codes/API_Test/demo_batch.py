import os
import base64
import requests

from utils import client


# base64编码函数
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# 图片目录地址
colormap_name = 'gray'
shape = (820, 630)
res = (2, 2)
octaves = 5
res_list = [(2, 2), (4, 4), (6, 6)]  # 基础网格分辨率
octaves_list = [1, 3, 5]
prepath = f'E:\\桌面\\Final project\\color\\{colormap_name}\\{shape}{res}{octaves}'
image_path = f"{prepath}\\scalar_field_{colormap_name}_{shape}_{res}_{octaves}.png" # 图片文件夹路径
base64_image = encode_image(image_path)
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text",
                 "text": """The image has dimensions of 820x630 and uses the 'gray' colormap. 
                 The data has been normalized. Please identify and mark points on the image corresponding to the data values 
                 1.0, 0.8, 0.6, 0.4, and 0.2. Provide the coordinates of the marked points. 
                 Avoid selecting points near the edges of the image and try to distribute the marked points across different areas. 
                 Only one point should be provided for each value. 
                 Please limit the output coordinate format to 1.0: (200, 150)."""
                 },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpg;base64,{base64_image}"},
                },
            ],
        }
    ],
)

output_path = f"E:\\桌面\\Final project\\result\\{colormap_name}_{shape}_{res}_{octaves}.txt"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(response.choices[0].message.content + "\n")

print(f"Result written to {output_path}")
