package com.translation.api.controller;

import com.translation.api.model.Language;
import com.translation.api.model.TranslationRequest;
import com.translation.api.model.TranslationResponse;
import com.translation.api.service.TranslationService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Arrays;
import java.util.List;

@RestController
@RequestMapping("/v2")
public class TranslationController {
    
    private final TranslationService translationService;
    
    public TranslationController(TranslationService translationService) {
        this.translationService = translationService;
    }
    
    @PostMapping("/translate")
    public ResponseEntity<TranslationResponse> translate(@Valid @RequestBody TranslationRequest request) {
        TranslationResponse response = translationService.translate(request);
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/languages")
    public ResponseEntity<List<Language>> getLanguages(@RequestParam(required = false) String type) {
        List<Language> languages = Arrays.asList(
            new Language("EN", "English", false),
            new Language("DE", "German", false),
            new Language("FR", "French", false),
            new Language("ES", "Spanish", false),
            new Language("IT", "Italian", false),
            new Language("PT", "Portuguese", false),
            new Language("NL", "Dutch", false),
            new Language("PL", "Polish", false),
            new Language("RU", "Russian", false),
            new Language("JA", "Japanese", false),
            new Language("ZH", "Chinese", false),
            new Language("AR", "Arabic", false),
            new Language("HI", "Hindi", false),
            new Language("TR", "Turkish", false),
            new Language("KO", "Korean", false)
        );
        return ResponseEntity.ok(languages);
    }
}
