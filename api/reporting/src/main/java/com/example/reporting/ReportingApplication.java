package com.example.reporting;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;
import java.util.*;

@SpringBootApplication
@RestController
@RequestMapping("/reports")
public class ReportingApplication {
    public static void main(String[] args) { SpringApplication.run(ReportingApplication.class, args); }
    @GetMapping("/health") public Map<String,Object> health() { return Map.of("status","ok"); }

    @GetMapping("/{userId}") 
    public Map<String,Object> getReport(@PathVariable String userId) {
        // Dummy report data
        return Map.of("userId", userId, "reportData", List.of(100, 110, 105, 115, 120));
    }
}