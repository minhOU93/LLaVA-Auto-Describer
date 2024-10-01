##################################
# Code provided by Venelin Valkov
##################################

from llava.model.builder import load_pretrained_model
from llava.utils import disable_torch_init
from llava.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN, DEFAULT_IM_START_TOKEN, DEFAULT_IM_END_TOKEN
from llava.mm_utils import tokenizer_image_token, KeywordsStoppingCriteria, get_model_name_from_path, process_images
from llava.conversation import conv_templates, SeparatorStyle

import torch
from PIL import Image
import requests
from io import BytesIO
import time

disable_torch_init()

MODEL = "liuhaotian/llava-v1.6-34b"
model_name = get_model_name_from_path(MODEL)

tokenizer, model, image_processor, context_len = load_pretrained_model(
    model_path=MODEL, model_base=None, model_name=model_name, load_4bit=True
)

def load_image(image_file):
    image = Image.open(image_file).convert("RGB")
    return image

def process_image(image):
    args = {"image_aspect_ratio": "pad"}
    image_tensor = process_images([image], image_processor, args)
    return image_tensor.to(model.device, dtype=torch.float16)

CONV_MODE = "llava_v0"

def create_prompt(prompt):
    conv = conv_templates[CONV_MODE].copy()
    roles = conv.roles
    prompt = DEFAULT_IMAGE_TOKEN + "\n" + prompt
    conv.append_message(roles[0], prompt)
    conv.append_message(roles[1], None)
    return conv.get_prompt(), conv

def ask_image(image: Image, prompt: str):
    image_tensor = process_image(image)
    prompt, conv = create_prompt(prompt)
    input_ids = (
        tokenizer_image_token(prompt, tokenizer, IMAGE_TOKEN_INDEX, return_tensors="pt")
        .unsqueeze(0)
        .to(model.device)
    )

    stop_str = conv.sep if conv.sep_style != SeparatorStyle.TWO else conv.sep2
    stopping_criteria = KeywordsStoppingCriteria(
        keywords=[stop_str], tokenizer=tokenizer, input_ids=input_ids
    )

    with torch.inference_mode():
        output_ids = model.generate(
            input_ids,
            images=image_tensor,
            do_sample=True,
            temperature=0.01,
            max_new_tokens=512,
            use_cache=True,
            stopping_criteria=[stopping_criteria]
        )

    text_outputs = tokenizer.batch_decode(output_ids, skip_special_tokens=True)

    return text_outputs[0][0:len(text_outputs[0]) - 3]
    # return tokenizer.decode(
    #     output_ids[0, input_ids.shape[1] :], skip_special_tokens=True
    # ).strip()

#result = ask_image(image, "Describe the image")
#print(result)
