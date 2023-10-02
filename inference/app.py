import requests
import json
import random
import gradio as gr
from PIL import Image
from io import BytesIO


ENDPOINT = "xxxxxxxxxxxxxxxxxxx"
TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxx"


def deliver_request(style, desc):
    number = random.randint(1, 90) % 3
    print("node: ", number)
    return generate_figure(style, desc)


def generate_figure(style, desc):
    requests_json = {
        "style": style,
        "desc": desc
    }

    headers = {
        "Content-Type": "application/json",
        "token": TOKEN
    }

    response = requests.post(ENDPOINT, json=requests_json, headers=headers, verify=False)
    response = json.loads(response.text)

    url_dict = response["data"]["pictures"]
    image_list = []
    for k in url_dict:
        image_list.append(Image.open(BytesIO(requests.get(url_dict[k]).content)))

    return image_list


def read_content(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    return content


examples_style = ["科幻 赛博朋克", "赛博朋克", "未来世界"]
examples_desc = ["城市夜景", "大象", "一只猫", "摩天大楼", "机甲熊猫"]

css = """
.gradio-container {background-image: url('file=./background.jpg'); background-size:cover; background-repeat: no-repeat;}

#generate {
    background: linear-gradient(#D8C5EB, #C5E8EB，#90CCF6);
    border: 1px solid #C5E8EB;
    border-radius: 8px;
    color: #26498B
}
"""


with gr.Blocks(css=css) as demo:
    gr.Markdown("# MindSpore Wukong-Huahua "
                "\nWukong-Huahua is a diffusion-based model that perfoms text-to-image task in Chinese, "
                "It was trained on Wukong dataset and used MindSpore + Ascend,")

    with gr.Tab("图片生成 (Figure Generation)"):

        style_input = gr.Textbox(lines=1,
                                 placeholder="输入中文风格描述",
                                 label="Input the style of figure you want to generate. (use Chinese better)",
                                 elem_id="style-input")
        gr.Examples(
            examples=examples_style,
            inputs=style_input,
        )
        with gr.Row():
            gr.Markdown(" *** ")
        desc_input = gr.Textbox(lines=1,
                                placeholder="输入中文图片描述",
                                label="Input a sentence to describe the figure you want to generate. "
                                      "(use Chinese better)")
        gr.Examples(
            examples=examples_desc,
            inputs=desc_input,
        )
        generate_button = gr.Button("Generate", elem_id="generate")
        with gr.Row():
            img_output1 = gr.Image(type="pil")
            img_output2 = gr.Image(type="pil")
            img_output3 = gr.Image(type="pil")
            img_output4 = gr.Image(type="pil")

    with gr.Accordion("Open for More!"):
        gr.Markdown("- If you want to know more about the foundation models of MindSpore, please visit "
                    "[The Foundation Models Platform for Mindspore](https://xihe.mindspore.cn/)")

    generate_button.click(deliver_request,
                          inputs=[style_input, desc_input],
                          outputs=[img_output1, img_output2, img_output3, img_output4])

demo.queue(concurrency_count=5)
demo.launch.queue()
