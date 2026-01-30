package com.translation.api.service;

import com.translation.api.model.Translation;
import com.translation.api.model.TranslationRequest;
import com.translation.api.model.TranslationResponse;
import com.translation.api.model.AiTranslationResponse;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class TranslationService {
    
    private final AiTranslationService aiTranslationService;
    
    public TranslationService(AiTranslationService aiTranslationService) {
        this.aiTranslationService = aiTranslationService;
    }
    
    public TranslationResponse translate(TranslationRequest request) {
        List<Translation> translations = new ArrayList<>();
        
        for (String text : request.getText()) {
            AiTranslationResponse aiResponse = aiTranslationService.translate(
                text,
                request.getSource_lang(),
                request.getTarget_lang()
            );
            
            Translation translation = Translation.builder()
                .text(aiResponse.getTranslatedText())
                .detected_source_language(aiResponse.getDetectedSourceLanguage())
                .build();
            
            translations.add(translation);
        }
        
        return TranslationResponse.builder()
            .translations(translations)
            .build();
    }
}
