package com.translation.api.model;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class AiTranslationRequest {
    private String text;
    private String sourceLang;
    private String targetLang;
}
