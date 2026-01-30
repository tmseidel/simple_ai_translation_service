#!/bin/bash

# Simple test script for the Translation API

API_URL="http://localhost:8080"

echo "Testing Translation API..."
echo "=========================="
echo ""

# Test 1: Health check (languages endpoint)
echo "Test 1: Getting supported languages..."
LANGUAGES=$(curl -s "${API_URL}/v2/languages")
if [ $? -eq 0 ]; then
    echo "✓ Languages endpoint working"
    echo "  Available languages: $(echo $LANGUAGES | grep -o '"language":"[^"]*"' | wc -l)"
else
    echo "✗ Languages endpoint failed"
fi
echo ""

# Test 2: Simple translation
echo "Test 2: Translating 'Hello World' to German..."
RESPONSE=$(curl -s -X POST "${API_URL}/v2/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": ["Hello World"],
    "target_lang": "DE"
  }')

if [ $? -eq 0 ] && echo "$RESPONSE" | grep -q "translations"; then
    echo "✓ Translation successful"
    TRANSLATED_TEXT=$(echo $RESPONSE | grep -o '"text":"[^"]*"' | head -1 | cut -d'"' -f4)
    echo "  Translation: $TRANSLATED_TEXT"
else
    echo "✗ Translation failed"
    echo "  Response: $RESPONSE"
fi
echo ""

# Test 3: Multiple texts
echo "Test 3: Translating multiple texts to Spanish..."
RESPONSE=$(curl -s -X POST "${API_URL}/v2/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": ["Good morning", "Good night"],
    "target_lang": "ES"
  }')

if [ $? -eq 0 ] && echo "$RESPONSE" | grep -q "translations"; then
    COUNT=$(echo $RESPONSE | grep -o '"text":"[^"]*"' | wc -l)
    echo "✓ Multiple translations successful"
    echo "  Translated $COUNT texts"
else
    echo "✗ Multiple translations failed"
fi
echo ""

echo "=========================="
echo "Testing complete!"
