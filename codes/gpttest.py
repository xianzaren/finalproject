from openai import OpenAI
import os
import base64

client = OpenAI(
    api_key="sk-aoVUFXxLA9UfcZk5BAf33vQ0A0Ljjase8iLsPFwetntzdnoa"
)


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

colormap_name = 'gray'
shape = (820, 630)
res = (2, 2)
octaves = 5
res_list = [(2, 2), (4, 4), (6, 6)]  # 基础网格分辨率
octaves_list = [1, 3, 5]
prepath = f'../color\\{colormap_name}\\{shape}{res}{octaves}'
fig_path = f"../result"

for filename in os.listdir(fig_path):
    if filename.endswith('.png'):
        image_path = os.path.join(fig_path, filename)
        print(image_path)
        base64_image = encode_image(image_path)
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": """The image has dimensions of 820x630 and uses the 'gray' colormap. 
                 The data has been normalized. Please identify and mark points on the image corresponding to the data values 
                 1.0, 0.8, 0.6, 0.4, and 0.2. Provide the coordinates of the marked points. 
                 Avoid selecting points near the edges of the image and try to distribute the marked points across different areas. 
                 Only one point should be provided for each value. 
                 Please limit the output coordinate format to 1.0: (200, 150)."""},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        chat_response = completion
        answer = chat_response.choices[0].message.content
        print(f'ChatGPT: {answer}')