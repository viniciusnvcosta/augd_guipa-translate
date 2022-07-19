import os
import torch
import gradio as gr
import time
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from flores200_codes import flores_codes


def load_models():
    # build model and tokenizer
    model_name_dict = {'nllb-distilled-600M': 'facebook/nllb-200-distilled-600M',
                  'nllb-1.3B': 'facebook/nllb-200-1.3B',
                  'nllb-distilled-1.3B': 'facebook/nllb-200-distilled-1.3B',
                  #'nllb-3.3B': 'facebook/nllb-200-3.3B',
                  }

    model_dict = {}

    for call_name, real_name in model_name_dict.items():
        print('\tLoading model: %s' % call_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(real_name)
        tokenizer = AutoTokenizer.from_pretrained(real_name)
        model_dict[call_name+'_model'] = model
        model_dict[call_name+'_tokenizer'] = tokenizer

    return model_dict


def translation(model_name, source, target, text):
    start_time = time.time()
    source = flores_codes[source]
    target = flores_codes[target]

    model = model_dict[model_name + '_model']
    tokenizer = model_dict[model_name + '_tokenizer']

    translator = pipeline('translation', model=model, tokenizer=tokenizer, src_lang=source, tgt_lang=target)
    output = translator(text, max_length=400)

    end_time = time.time()

    output = output[0]['translation_text']
    result = {'inference_time': end_time - start_time,
              'source': source,
              'target': target,
              'result': output}
    return result


if __name__ == '__main__':
    print('\tinit models')

    global model_dict

    model_dict = load_models()
    
    # define gradio demo
    lang_codes = list(flores_codes.keys())
    inputs = [gr.inputs.Radio(['nllb-distilled-600M', 'nllb-1.3B', 'nllb-distilled-1.3B'], label='NLLB Model'),
              gr.inputs.Dropdown(lang_codes, label='Source'),
              gr.inputs.Dropdown(lang_codes, label='Target'),
              gr.inputs.Textbox(lines=5, label="Input text"),
              ]

    outputs = gr.outputs.JSON()

    title = "NLLB demo"

    demo_status = "Demo is running on CPU"
    description = f"Details: https://github.com/facebookresearch/fairseq/tree/nllb. {demo_status}"
    examples = [
    ['nllb-distilled-600M', 'English', 'Korean', 'Hi. nice to meet you']
    ]

    gr.Interface(translation,
                 inputs,
                 outputs,
                 title=title,
                 description=description,
                 examples=examples,
                 examples_per_page=50,
                 ).launch()


