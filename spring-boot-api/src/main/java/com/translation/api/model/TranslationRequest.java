package com.translation.api.model;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import jakarta.validation.constraints.NotEmpty;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class TranslationRequest {
    @NotEmpty(message = "Text is required")
    private List<String> text;
    
    private String source_lang;
    
    @NotEmpty(message = "Target language is required")
    private String target_lang;
    
    private String formality;
    private String context;
    private String split_sentences;
    private String preserve_formatting;
}
