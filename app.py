import os
import torch
import gradio as gr
from gradio.components import (
    Textbox,
    TextboxGroup,
    CheckboxGroup,
    Radio,
    Dropdown,
    Image,
    ImageFolder,
)
import time
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from flores200_codes import flores_codes


def load_models():
    # build model and tokenizer
    model_name_dict = {
        "nllb-distilled-600M": "facebook/nllb-200-distilled-600M",
        #'nllb-1.3B': 'facebook/nllb-200-1.3B',
        #'nllb-distilled-1.3B': 'facebook/nllb-200-distilled-1.3B',
        #'nllb-3.3B': 'facebook/nllb-200-3.3B',
    }

    model_dict = {}

    for call_name, real_name in model_name_dict.items():
        print("\tLoading model: %s" % call_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(real_name)
        tokenizer = AutoTokenizer.from_pretrained(real_name)
        model_dict[call_name + "_model"] = model
        model_dict[call_name + "_tokenizer"] = tokenizer

    return model_dict


def translation(source, target, text):
    if len(model_dict) == 2:
        model_name = "nllb-distilled-600M"

    start_time = time.time()
    source = flores_codes[source]
    target = flores_codes[target]

    model = model_dict[model_name + "_model"]
    tokenizer = model_dict[model_name + "_tokenizer"]

    # TODO: pre-prompt text
    # get all the commented text
    # text = text.split('\n').where(lambda x: x.startswith('#'))

    translator = pipeline(
        "translation",
        model=model,
        tokenizer=tokenizer,
        src_lang=source,
        tgt_lang=target,
    )
    output = translator(text, max_length=400)

    end_time = time.time()

    output = output[0]["translation_text"]
    result = {
        "inference_time": end_time - start_time,
        "source": source,
        "target": target,
        "result": output,
    }
    return result


if __name__ == "__main__":
    print("\tinit models")

    global model_dict

    model_dict = load_models()

    # define gradio demo
    lang_codes = list(flores_codes.keys())
    inputs = [
        gr.inputs.Dropdown(lang_codes, label="Source", default="English", key="source"),
        gr.inputs.Dropdown(lang_codes, label="Target", default="Korean", key="target"),
        gr.inputs.Textbox(lines=5, label="Input text", key="text"),
    ]

    output = gr.outputs.Json(label="Output")

    title = "Guipa Translate demo"
    demo_status = "Demo is running on CPU"
    description = (
        f"Details: https://github.com/facebookresearch/fairseq/tree/nllb. {demo_status}"
    )

    examples = [["English", "Korean", "Hi. nice to meet you"]]

    iface = gr.Interface(
        fn=translation,
        inputs=inputs,
        output=output,
        title=title,
        description=description,
    )
    iface.launch()
