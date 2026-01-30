from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os
import logging
import time
import torch

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Model configuration
MODEL_NAME = os.environ.get("MODEL_NAME", "facebook/nllb-200-1.3B")
MODEL_LOAD_MAX_RETRIES = int(os.environ.get("MODEL_LOAD_MAX_RETRIES", "3"))
MODEL_LOAD_RETRY_DELAY_SEC = int(os.environ.get("MODEL_LOAD_RETRY_DELAY_SEC", "5"))
USE_CUDA = os.environ.get("USE_CUDA", "true").lower() in ("1", "true", "yes", "on")

def _resolve_device():
    if USE_CUDA and torch.cuda.is_available():
        return "cuda"
    if USE_CUDA:
        logger.warning("CUDA requested but not available. Falling back to CPU. Set USE_CUDA=false to suppress this warning.")
    return "cpu"

DEVICE = _resolve_device()

# Language code mapping for NLLB (DeepL to NLLB format)
LANGUAGE_MAP = {
    'EN': 'eng_Latn',
    'DE': 'deu_Latn',
    'FR': 'fra_Latn',
    'ES': 'spa_Latn',
    'IT': 'ita_Latn',
    'PT': 'por_Latn',
    'NL': 'nld_Latn',
    'PL': 'pol_Latn',
    'RU': 'rus_Cyrl',
    'JA': 'jpn_Jpan',
    'ZH': 'zho_Hans',
    'AR': 'arb_Arab',
    'HI': 'hin_Deva',
    'TR': 'tur_Latn',
    'KO': 'kor_Hang'
}

# Reverse mapping for NLLB to DeepL format
REVERSE_LANGUAGE_MAP = {v: k for k, v in LANGUAGE_MAP.items()}

# Global variables for model and tokenizer
tokenizer = None
model = None

def _model_cached():
    try:
        AutoTokenizer.from_pretrained(MODEL_NAME, local_files_only=True)
        AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME, local_files_only=True)
        return True
    except Exception:
        return False

def load_model():
    """Load the NLLB model and tokenizer"""
    global tokenizer, model
    logger.info("Loading model: %s", MODEL_NAME)
    logger.info("Using device: %s", DEVICE)
    for attempt in range(1, MODEL_LOAD_MAX_RETRIES + 1):
        try:
            if _model_cached():
                logger.info("Model already cached locally.")
            else:
                logger.info("Model not cached. Downloading...")
            tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
            model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME).to(DEVICE)
            logger.info("Model loaded successfully")
            return
        except Exception as e:
            if attempt >= MODEL_LOAD_MAX_RETRIES:
                logger.error("Failed to load model after %s attempts: %s", attempt, e)
                raise
            logger.warning("Model load failed (attempt %s/%s). Retrying in %ss...", attempt, MODEL_LOAD_MAX_RETRIES, MODEL_LOAD_RETRY_DELAY_SEC)
            time.sleep(MODEL_LOAD_RETRY_DELAY_SEC)

# Load model at module import time
logger.info("Initializing AI Translation Service...")
load_model()

def get_nllb_language_code(lang_code):
    """Convert DeepL language code to NLLB format"""
    if not lang_code:
        return None
    upper_lang = lang_code.upper()
    return LANGUAGE_MAP.get(upper_lang, lang_code)

def translate_text(text, source_lang, target_lang):
    """Translate text using NLLB model"""
    try:
        # Convert language codes
        src_lang_code = get_nllb_language_code(source_lang)
        tgt_lang_code = get_nllb_language_code(target_lang)
        
        # If source language is not provided, use English as default
        if not src_lang_code:
            src_lang_code = 'eng_Latn'
        
        logger.info(f"Translating from {src_lang_code} to {tgt_lang_code}")
        
        # Tokenize
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512).to(DEVICE)
        
        # Translate
        translated_tokens = model.generate(
            **inputs,
            forced_bos_token_id=tokenizer.convert_tokens_to_ids(tgt_lang_code),
            max_length=512
        )
        
        # Decode
        translated_text = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
        
        return translated_text, src_lang_code
    except Exception as e:
        logger.error(f"Translation error: {e}")
        raise

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "model": MODEL_NAME, "device": DEVICE}), 200

@app.route('/translate', methods=['POST'])
def translate():
    """Translation endpoint"""
    try:
        data = request.json
        
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        text = data.get('text')
        target_lang = data.get('targetLang')
        source_lang = data.get('sourceLang')
        
        if not text:
            return jsonify({"error": "Field 'text' is required and cannot be empty"}), 400
        
        if not target_lang:
            return jsonify({"error": "Field 'targetLang' is required and cannot be empty"}), 400
        
        # Translate
        translated_text, detected_source = translate_text(text, source_lang, target_lang)
        
        # Prepare response
        response = {
            "translatedText": translated_text,
            "detectedSourceLanguage": REVERSE_LANGUAGE_MAP.get(detected_source, "EN")
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error in translate endpoint: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
