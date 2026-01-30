package com.translation.api.service;

import com.translation.api.model.AiTranslationRequest;
import com.translation.api.model.AiTranslationResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.time.Duration;

@Service
public class AiTranslationService {
    
    @Value("${ai.service.url}")
    private String aiServiceUrl;
    
    private final RestTemplate restTemplate;
    
    public AiTranslationService(RestTemplateBuilder restTemplateBuilder) {
        this.restTemplate = restTemplateBuilder
            .setConnectTimeout(Duration.ofSeconds(10))
            .setReadTimeout(Duration.ofSeconds(300))
            .build();
    }
    
    public AiTranslationResponse translate(String text, String sourceLang, String targetLang) {
        AiTranslationRequest request = new AiTranslationRequest(text, sourceLang, targetLang);
        
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<AiTranslationRequest> entity = new HttpEntity<>(request, headers);
        
        try {
            return restTemplate.postForObject(
                aiServiceUrl + "/translate",
                entity,
                AiTranslationResponse.class
            );
        } catch (Exception e) {
            throw new RuntimeException("Failed to call AI translation service: " + e.getMessage(), e);
        }
    }
}
