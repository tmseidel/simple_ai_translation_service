package com.translation.api.model;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Language {
    private String language;
    private String name;
    private Boolean supportsFormality;
}
