# Simple AI Translation Service

A self-hosted AI-backed translation service compatible with the DeepL REST API interface. This service uses the NLLB-200 (No Language Left Behind) distilled AI model from Meta for high-quality neural machine translation.

## Features

- **DeepL-Compatible REST API**: Drop-in replacement for DeepL API endpoints
- **NLLB-200 Model**: State-of-the-art neural machine translation supporting 200+ languages
- **Containerized Architecture**: Easy deployment with Docker and Docker Compose
- **Spring Boot Backend**: Robust Java REST API
- **Python AI Service**: Efficient translation service using Transformers
- **API Testing**: Includes Bruno collection for easy API testing

## Architecture

The service consists of two main components:

1. **Spring Boot REST API** (`spring-boot-api/`): Handles HTTP requests and provides a DeepL-compatible interface
2. **Python AI Service** (`ai-service/`): Performs actual translation using the NLLB-200 model

```
Client → Spring Boot API (Port 8080) → Python AI Service (Port 5000) → NLLB-200 Model
```

## Supported Languages

The service supports the following languages (with their DeepL-style codes):

- EN (English)
- DE (German)
- FR (French)
- ES (Spanish)
- IT (Italian)
- PT (Portuguese)
- NL (Dutch)
- PL (Polish)
- RU (Russian)
- JA (Japanese)
- ZH (Chinese)
- AR (Arabic)
- HI (Hindi)
- TR (Turkish)
- KO (Korean)

## Prerequisites

- Docker and Docker Compose
- At least 4GB of RAM available for Docker
- Approximately 2GB of disk space for the AI model

## Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tmseidel/simple_ai_translation_service.git
   cd simple_ai_translation_service
   ```

2. **Build and start the services**:
   ```bash
   docker-compose up --build
   ```

   The first startup will take several minutes as it downloads the NLLB-200 model (~1.2GB).

3. **Wait for services to be ready**:
   - AI Service: http://localhost:5000/health
   - REST API: http://localhost:8080/v2/languages

4. **Test the API**:
   ```bash
   curl -X POST http://localhost:8080/v2/translate \
     -H "Content-Type: application/json" \
     -d '{
       "text": ["Hello, how are you?"],
       "target_lang": "DE"
     }'
   ```

## API Usage

### Translate Text

**Endpoint**: `POST /v2/translate`

**Request Body**:
```json
{
  "text": ["Hello, how are you?", "This is a test."],
  "source_lang": "EN",
  "target_lang": "DE"
}
```

**Response**:
```json
{
  "translations": [
    {
      "detected_source_language": "EN",
      "text": "Hallo, wie geht es dir?"
    },
    {
      "detected_source_language": "EN",
      "text": "Das ist ein Test."
    }
  ]
}
```

### Get Supported Languages

**Endpoint**: `GET /v2/languages`

**Response**:
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

## Bruno API Collection

A Bruno API collection is provided in the `bruno-collection/` directory for easy API testing.

### Using Bruno

1. **Install Bruno**: Download from https://www.usebruno.com/
2. **Open Collection**: Open Bruno and import the `bruno-collection` folder
3. **Run Requests**: Execute the pre-configured API requests

Available requests:
- **Translate Text**: Basic translation request
- **Translate with Source Language**: Translation with explicit source language
- **Get Supported Languages**: List all supported languages
- **Multiple Language Translation**: Translate multiple texts at once

## Development

### Spring Boot API

**Build**:
```bash
cd spring-boot-api
mvn clean package
```

**Run locally** (requires AI service running):
```bash
java -jar target/translation-api-1.0.0.jar
```

### Python AI Service

**Setup**:
```bash
cd ai-service
pip install -r requirements.txt
```

**Run locally**:
```bash
python app.py
```

## Docker Commands

**Build only**:
```bash
docker-compose build
```

**Start in detached mode**:
```bash
docker-compose up -d
```

**View logs**:
```bash
docker-compose logs -f
```

**Stop services**:
```bash
docker-compose down
```

**Rebuild and restart**:
```bash
docker-compose down
docker-compose up --build
```

## Configuration

### Spring Boot API

Configuration file: `spring-boot-api/src/main/resources/application.properties`

Key settings:
- `server.port`: API port (default: 8080)
- `ai.service.url`: URL of the AI service (default: http://ai-service:5000)

### AI Service

Environment variables:
- `PORT`: Service port (default: 5000)

## Troubleshooting

### Service fails to start

1. Check Docker logs: `docker-compose logs`
2. Ensure sufficient memory is allocated to Docker
3. Verify ports 8080 and 5000 are not in use

### Translation is slow

- First translation is slower as the model initializes
- Subsequent translations are faster due to model caching
- Consider increasing Docker memory allocation

### Model download fails

- Check internet connection
- Verify sufficient disk space
- The model is downloaded during Docker build time

## Performance Notes

- **First Request**: May take 30-60 seconds as the model loads
- **Subsequent Requests**: Typically complete in 1-3 seconds
- **Memory Usage**: AI service requires ~2-3GB RAM
- **Concurrent Requests**: Limited by available resources

## License

This project is provided as-is for self-hosting purposes.

## Credits

- **NLLB-200 Model**: Meta AI Research
- **Transformers Library**: Hugging Face
- **Spring Boot**: Pivotal Software

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Support

For issues and questions, please use the GitHub issue tracker.
