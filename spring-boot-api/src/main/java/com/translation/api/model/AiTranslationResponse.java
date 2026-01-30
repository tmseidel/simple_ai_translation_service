package com.translation.api.model;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class AiTranslationResponse {
    private String translatedText;
    private String detectedSourceLanguage;
}
