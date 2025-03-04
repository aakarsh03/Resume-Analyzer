package com.resume.enhancer.resume_backend.controller;

import com.resume.enhancer.resume_backend.service.ResumeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/resume")
public class ResumeController {

    @Autowired
    private ResumeService resumeService;

    // Updated method to accept both the resume file and job description
    @PostMapping("/analyze")
    public ResponseEntity<String> analyzeResume(
            @RequestParam("file") MultipartFile file, 
            @RequestParam("jobDescription") String jobDescription) {

        // Process the resume and job description and return the response
        String response = resumeService.processResume(file, jobDescription);
        return ResponseEntity.ok(response);
    }
}
