# Component & Dependency Details

This document provides a deeper, developer-focused explanation of the core components, how they work together, and why each Python dependency exists. It is aimed at Java developers who want to understand the AI-specific pieces without needing deep ML knowledge.

## System Components and Usage

### 1) Spring Boot REST API (`spring-boot-api/`)

**Purpose:** Provide a DeepL-compatible REST interface and translate requests into calls to the AI service.

**Key classes and responsibilities:**
- **`TranslationController`** (`spring-boot-api/src/main/java/com/translation/api/controller/TranslationController.java`)
  - Exposes **`POST /v2/translate`** and **`GET /v2/languages`**.
  - Accepts a JSON request with `text[]`, `source_lang`, and `target_lang`.
- **`TranslationService`** (`spring-boot-api/src/main/java/com/translation/api/service/TranslationService.java`)
  - Iterates over each input text and calls the AI service once per item.
  - Builds the DeepL-style response array.
- **`AiTranslationService`** (`spring-boot-api/src/main/java/com/translation/api/service/AiTranslationService.java`)
  - Uses `RestTemplate` with timeouts (10s connect / 300s read).
  - Sends JSON to `POST /translate` in the Python service and returns the mapped response.

**Typical usage flow (HTTP):**
1. Client sends `POST /v2/translate` with the DeepL-style payload.
2. Spring Boot validates the request and forwards each text to the AI service.
3. Spring Boot returns a DeepL-compatible response to the client.

### 2) Python AI Service (`ai-service/`)

**Purpose:** Perform the actual machine translation using Meta’s NLLB-200 model.

**Key functions and responsibilities (in `ai-service/app.py`):**
- **`load_model()`**
  - Uses Hugging Face `AutoTokenizer` and `AutoModelForSeq2SeqLM` to load the model.
  - Runs once at startup so translations are fast afterward.
- **`translate_text(text, source_lang, target_lang)`**
  - Maps language codes (e.g., `DE` → `deu_Latn`) using `LANGUAGE_MAP`.
  - Tokenizes input text (`tokenizer(..., max_length=512)`).
  - Calls `model.generate(...)` to produce translated tokens.
  - Decodes tokens back to text and returns it.
- **`POST /translate`**
  - Accepts JSON: `{ "text": "...", "sourceLang": "EN", "targetLang": "DE" }`
  - Returns JSON: `{ "translatedText": "...", "detectedSourceLanguage": "EN" }`

**Usage tip:** When running locally, start the AI service first so the Spring API can reach it.

## What “Transformer” Means Here

The NLLB-200 model is a **transformer-based sequence-to-sequence model**. In practical terms:

1. **Tokenization**  
   Text is converted to tokens (integer IDs). NLLB uses **SentencePiece** under the hood for multilingual tokenization.

2. **Encoder/Decoder with Self-Attention**  
   - The **encoder** reads the input tokens and builds a contextual representation.  
   - The **decoder** generates output tokens one at a time while attending to the encoder output.  
   - “Self-attention” lets the model focus on important parts of the input (e.g., word order, phrases).

3. **Generation**  
   The `model.generate(...)` call performs the decoding loop. In this project we set
   `forced_bos_token_id` so the model starts decoding in the *target language*.

In short: a transformer is the neural network architecture that enables high-quality translation by “paying attention” to the full input sequence while generating output tokens.

## Why Each `requirements.txt` Dependency Exists

| Dependency | Why it is needed | Where it is used |
| --- | --- | --- |
| **flask** | Lightweight HTTP server and routing for `/translate` and `/health`. | `ai-service/app.py` |
| **transformers** | Hugging Face model + tokenizer APIs (`AutoTokenizer`, `AutoModelForSeq2SeqLM`). | `ai-service/app.py`, `ai-service/Dockerfile` |
| **torch** | PyTorch runtime that powers model inference and tensor operations. | Indirectly used by `transformers` |
| **sentencepiece** | Tokenization engine required by NLLB and Hugging Face tokenizers. | Indirectly used by `transformers` |
| **protobuf** | Serialization format used by model configs and tokenizer assets. Required by `transformers`. | Dependency of `transformers` |
| **gunicorn** | Production-grade WSGI server (used in Docker `CMD`). | `ai-service/Dockerfile` |

If you remove any of these, the model either cannot load, cannot tokenize, or the service cannot start.
