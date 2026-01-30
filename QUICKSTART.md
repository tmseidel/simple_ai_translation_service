# Quick Start Guide

This guide will help you get the Translation API up and running in minutes.

## Prerequisites

### Option A: Docker (containerized)

1. **Docker Desktop** (or Docker Engine + Docker Compose)
   - Windows/Mac: Download from https://www.docker.com/products/docker-desktop
   - Linux: Install docker and docker-compose packages

2. **System Requirements**
   - At least 4GB of available RAM
   - 3GB of free disk space
   - Internet connection (for initial model download)

### Option B: Native install (Ansible)

1. **Remote Debian/Ubuntu host** with systemd
2. **Ansible 2.15+** on your control machine
3. **System Requirements**
   - At least 4GB of available RAM
   - 3GB of free disk space
   - Internet connection (for initial model download)

## Step-by-Step Setup

### 1. Clone or Download

```bash
git clone https://github.com/tmseidel/simple_ai_translation_service.git
cd simple_ai_translation_service
```

### 2. Start the Services

```bash
docker compose up --build
```

**What happens now:**
- Docker builds two images (Spring Boot API and Python AI Service)
- Downloads the NLLB-200 model (~2.4GB for the default) - this happens once during build
- Starts both services
- First startup takes 5-10 minutes

### 3. Wait for Services to Start

Watch the logs. You'll see:

```
ai-translation-service  | Model loaded successfully
translation-api         | Started TranslationApiApplication
```

### 4. Test the API

Open a new terminal and run:

```bash
# Test 1: Check if API is running
curl http://localhost:8080/health

# Test 2: Get supported languages
curl http://localhost:8080/v2/languages

# Test 3: Translate text
curl -X POST http://localhost:8080/v2/translate \
  -H "Content-Type: application/json" \
  -d '{
    "text": ["Hello, how are you?"],
    "target_lang": "DE"
  }'
```

Or use the provided test script:

```bash
chmod +x test-api.sh
./test-api.sh
```

### 5. Use Bruno for API Testing

1. Download Bruno from https://www.usebruno.com/
2. Open Bruno
3. Click "Open Collection"
4. Navigate to the `bruno-collection` folder
5. Try the pre-configured requests

## Native Deployment with Ansible (No Docker)

1. Update the inventory and variables:
   - `ansible/inventory.ini`
   - `ansible/group_vars/all.yml` (repo URL, service ports, model name, `use_cuda`, cache path)
   - `ansible/templates/*.service.j2` for systemd overrides

2. Run the playbook from the repository root:
   ```bash
   ansible-playbook -i ansible/inventory.ini ansible/playbook.yml
   ```
   For a one-off host/user/key without editing the inventory:
   ```bash
   ansible-playbook -i "translation.example.com," \
     -u ubuntu \
     --private-key ~/.ssh/translation.pem \
     ansible/playbook.yml
   ```

3. Validate services:
   - `curl http://<server>:8080/health`
   - `curl http://<server>:8080/v2/languages`

4. Optional GPU/system validation on the target host (checks CUDA, GPU drivers, and FP16 support):
   ```bash
   python ai-service/system_check.py
   ```

## Common Issues

### Port Already in Use

If ports 8080 or 5000 are already in use, modify `docker-compose.yml`:

```yaml
ports:
  - "8081:8080"  # Change 8080 to 8081 or any available port
```

### Out of Memory

Increase Docker memory limit:
- Docker Desktop: Settings → Resources → Memory → Increase to at least 4GB
- Linux: Adjust Docker daemon settings

### Model Download Fails

If the model download fails during build:

1. Check your internet connection
2. Try building again (Docker caches layers)
3. Or download the model manually and modify the Dockerfile

## Stopping the Services

```bash
# Stop services
docker compose down

# Stop and remove volumes (clean slate)
docker compose down -v
```

## Configuring the AI Model

To select a different NLLB model, set `MODEL_NAME` in `docker-compose.yml` or your environment, for example:

```bash
MODEL_NAME=facebook/nllb-200-distilled-600M docker compose up --build
```

## Next Steps

- Check out the [full README](README.md) for detailed API documentation
- Explore the Bruno collection for more API examples
- Configure the services (see Configuration section in README)

## Getting Help

If you encounter issues:
1. Check the logs: `docker compose logs`
2. Verify Docker is running: `docker ps`
3. Check GitHub issues: https://github.com/tmseidel/simple_ai_translation_service/issues
