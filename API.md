# API Documentation

This document describes the REST API endpoints provided by the Translation Service.

## Base URL

```
http://localhost:8080
```

## Endpoints

### 1. Health Check

Check if the API is running.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "UP",
  "service": "translation-api"
}
```

**HTTP Status Codes:**
- `200 OK`: Service is healthy

---

### 2. Translate Text

Translate one or more texts from a source language to a target language.

**Endpoint:** `POST /v2/translate`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "text": ["Text to translate", "Another text"],
  "source_lang": "EN",
  "target_lang": "DE",
  "formality": "default",
  "split_sentences": "1",
  "preserve_formatting": "1"
}
```

**Request Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | array of strings | Yes | The text(s) to be translated |
| `target_lang` | string | Yes | Target language code (e.g., "DE", "FR", "ES") |
| `source_lang` | string | No | Source language code. If not specified, language will be auto-detected |
| `formality` | string | No | Formality level (not yet supported by NLLB) |
| `split_sentences` | string | No | How to handle sentence splitting (not yet implemented) |
| `preserve_formatting` | string | No | Whether to preserve text formatting (not yet implemented) |

**Response:**
```json
{
  "translations": [
    {
      "detected_source_language": "EN",
      "text": "Hallo, wie geht es dir?"
    },
    {
      "detected_source_language": "EN",
      "text": "Ein weiterer Text"
    }
  ]
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `translations` | array | Array of translation objects |
| `translations[].text` | string | The translated text |
| `translations[].detected_source_language` | string | The detected source language code |

**HTTP Status Codes:**
- `200 OK`: Translation successful
- `400 Bad Request`: Invalid request (missing required fields)
- `500 Internal Server Error`: Translation failed

**Example Request (curl):**

```bash
curl -X POST http://localhost:8080/v2/translate \
  -H "Content-Type: application/json" \
  -d '{
    "text": ["Hello, how are you?"],
    "target_lang": "DE"
  }'
```

**Example Response:**
```json
{
  "translations": [
    {
      "detected_source_language": "EN",
      "text": "Hallo, wie geht es dir?"
    }
  ]
}
```

---

### 3. Get Supported Languages

Get a list of all supported languages.

**Endpoint:** `GET /v2/languages`

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `type` | string | No | Filter by language type (not implemented, for DeepL compatibility) |

**Response:**
```json
[
  {
    "language": "EN",
    "name": "English",
    "supportsFormality": false
  },
  {
    "language": "DE",
    "name": "German",
    "supportsFormality": false
  }
]
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `language` | string | Language code |
| `name` | string | Human-readable language name |
| `supportsFormality` | boolean | Whether the language supports formality settings |

**HTTP Status Codes:**
- `200 OK`: Request successful

**Example Request (curl):**

```bash
curl http://localhost:8080/v2/languages
```

---

## Supported Languages

| Code | Language |
|------|----------|
| EN | English |
| DE | German |
| FR | French |
| ES | Spanish |
| IT | Italian |
| PT | Portuguese |
| NL | Dutch |
| PL | Polish |
| RU | Russian |
| JA | Japanese |
| ZH | Chinese |
| AR | Arabic |
| HI | Hindi |
| TR | Turkish |
| KO | Korean |

## Error Handling

### Validation Errors

**HTTP Status:** `400 Bad Request`

**Response:**
```json
{
  "text": "Text is required",
  "target_lang": "Target language is required"
}
```

### Translation Errors

**HTTP Status:** `500 Internal Server Error`

**Response:**
```json
{
  "error": "Failed to call AI translation service: Connection refused"
}
```

## Rate Limiting

Currently, there is no rate limiting implemented. Consider adding rate limiting in production deployments.

## Authentication

Currently, the API does not require authentication. For production use, consider adding:
- API key authentication
- OAuth 2.0
- IP whitelisting

## DeepL Compatibility

This API is designed to be compatible with the DeepL API v2. The following endpoints are supported:

- ✅ `POST /v2/translate` - Full compatibility
- ✅ `GET /v2/languages` - Full compatibility
- ❌ `POST /v2/document` - Not implemented
- ❌ `POST /v2/document/{document_id}` - Not implemented
- ❌ `GET /v2/usage` - Not implemented

### Differences from DeepL

1. **Language Auto-detection**: Uses NLLB model's detection, may differ from DeepL
2. **Formality**: Not yet supported (NLLB limitation)
3. **Context**: Parameter accepted but not used
4. **Glossary**: Not supported
5. **Document Translation**: Not implemented

## Performance

- **First Request**: 30-60 seconds (model initialization)
- **Subsequent Requests**: 1-3 seconds per text
- **Concurrent Requests**: Limited by available resources (single worker by default)

## Examples

### Basic Translation

```bash
curl -X POST http://localhost:8080/v2/translate \
  -H "Content-Type: application/json" \
  -d '{
    "text": ["Hello World"],
    "target_lang": "FR"
  }'
```

### With Source Language

```bash
curl -X POST http://localhost:8080/v2/translate \
  -H "Content-Type: application/json" \
  -d '{
    "text": ["Bonjour"],
    "source_lang": "FR",
    "target_lang": "EN"
  }'
```

### Multiple Texts

```bash
curl -X POST http://localhost:8080/v2/translate \
  -H "Content-Type: application/json" \
  -d '{
    "text": [
      "Good morning",
      "Good evening",
      "Good night"
    ],
    "target_lang": "ES"
  }'
```

### Python Example

```python
import requests

url = "http://localhost:8080/v2/translate"
payload = {
    "text": ["Hello, how are you?"],
    "target_lang": "DE"
}
response = requests.post(url, json=payload)
print(response.json())
```

### JavaScript Example

```javascript
fetch('http://localhost:8080/v2/translate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    text: ['Hello, how are you?'],
    target_lang: 'DE'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```
