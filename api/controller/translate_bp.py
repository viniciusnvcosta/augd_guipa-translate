from flask import Blueprint, request
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


translate_bp = Blueprint('translate', __name__)

tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")


class Translate:
   @staticmethod
   @translate_bp.route('/translate', methods=['GET'])
   def get_translate():
      article = request.args.get("input",default=None)
      
      lang = request.args.get("lang",default="por_Latn")

      inputs = tokenizer(article, return_tensors="pt")

      translated_tokens = model.generate(
         **inputs, forced_bos_token_id=tokenizer.lang_code_to_id[lang], max_length=100_000
      )
         

      return tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
