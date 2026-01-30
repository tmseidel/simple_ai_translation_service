# Simple AI Translation Service

⚠️ **SECURITY NOTICE**: This project uses protobuf 4.25.8, which has a known JSON recursion depth bypass vulnerability with no available patch. This vulnerability has **LOW impact** on our use case (see [SECURITY.md](SECURITY.md) for details). All other dependencies are fully patched.

A self-hosted AI-backed translation service compatible with the DeepL REST API interface. This service uses the NLLB-200 (No Language Left Behind) AI model from Meta for high-quality neural machine translation.

## 📚 Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get started in 5 minutes
- **[API Documentation](API.md)** - Complete API reference
- **[Architecture Overview](ARCHITECTURE.md)** - System design and components

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
Client → Spring Boot API (Port 8080) → Python AI Service (Port 5000) → NLLB-200 Model (configurable)
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
- `MODEL_NAME`: Hugging Face model ID to load (default: `facebook/nllb-200-1.3B`)

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

## Security

⚠️ **IMPORTANT SECURITY NOTICE**

This project has **1 unpatched vulnerability** that cannot be fixed:

### Protobuf JSON Recursion Depth Bypass
- **Status**: ⚠️ NO PATCH AVAILABLE
- **Affected**: protobuf <= 6.33.4 (all versions)
- **Current version**: 4.25.8 (best available)
- **Risk level**: LOW for our use case
- **Why unfixable**: Vendor has not released a patch; affects all protobuf versions
- **Mitigation**: protobuf is only used for model serialization from trusted sources, not user input
- **Details**: See [SECURITY.md](SECURITY.md) for complete risk assessment

### Fully Patched Dependencies (13 vulnerabilities fixed)
- ✅ **gunicorn 22.0.0** (fixes HTTP Request/Response Smuggling vulnerabilities)
- ✅ **torch 2.6.0** (fixes buffer overflow, use-after-free, and RCE vulnerabilities)
- ✅ **transformers 4.48.0** (fixes deserialization vulnerabilities)
- ✅ **protobuf 4.25.8** (fixes 3 of 4 DoS vulnerabilities - 1 unfixable)
- ✅ **sentencepiece 0.2.1** (fixes heap overflow vulnerability)

**Note**: We are using the latest available versions of all dependencies. The protobuf issue affects the entire protobuf ecosystem and will be resolved when the vendor releases a patch.

For production deployments, we recommend:
1. Keep dependencies up to date with security patches
2. Add API key authentication
3. Configure specific CORS origins (not wildcard)
4. Implement rate limiting
5. Use HTTPS/TLS encryption
6. Add request validation and sanitization
7. Monitor and log all requests
8. Consider IP whitelisting for sensitive deployments

See [SECURITY.md](SECURITY.md) for comprehensive security guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

- **NLLB-200 Model**: Meta AI Research
- **Transformers Library**: Hugging Face
- **Spring Boot**: Pivotal Software

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Support

For issues and questions, please use the GitHub issue tracker.
