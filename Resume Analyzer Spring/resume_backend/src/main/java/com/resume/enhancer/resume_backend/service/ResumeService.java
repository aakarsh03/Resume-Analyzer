package com.resume.enhancer.resume_backend.service;

import com.resume.enhancer.resume_backend.utils.PdfParser;
import com.resume.enhancer.resume_backend.config.WebClientConfig;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.http.MediaType;
import org.springframework.web.reactive.function.BodyInserters;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Service
public class ResumeService {

    private final WebClient webClient;
    private static final Logger logger = LoggerFactory.getLogger(ResumeService.class);

    public ResumeService(WebClientConfig webClientConfig) {
        this.webClient = webClientConfig.webClient();
    }

    public String processResume(MultipartFile file, String jobDescription) {
        try {
            // Step 1: Extract text from the resume file
            String extractedText = PdfParser.extractText(file);
            
            // Log the extracted text length (not the full text to avoid large logs)
            logger.info("Extracted text length: {}", extractedText.length());

            // Step 2: Send the extracted text and job description to the Google Gemini API for analysis
            return callGoogleGeminiAPI(extractedText, jobDescription);
        } catch (Exception e) {
            // Log the error with detailed information
            logger.error("Error processing resume", e);
            return "Error processing resume: " + e.getMessage();
        }
    }

    private String callGoogleGeminiAPI(String resumeText, String jobDescription) {
        try {
            // Step 3: Call the external Google Gemini API using WebClient
            return webClient.post()
                    .uri("/analyze")  // Relative URL, as the base URL is already set in WebClientConfig
                    .contentType(MediaType.APPLICATION_JSON)  // Assuming the API expects JSON
                    .body(BodyInserters.fromValue(createRequestPayload(resumeText, jobDescription)))
                    .retrieve()
                    .bodyToMono(String.class)
                    .block();  // Use blocking call for testing; consider async approach for production

        } catch (Exception e) {
            // Log the error for API call failure
            logger.error("Error calling Google Gemini API", e);
            return "Error calling Google Gemini API: " + e.getMessage();
        }
    }

    // Helper method to create the JSON payload for the API request
    private Object createRequestPayload(String resumeText, String jobDescription) {
        // Assuming this is the expected structure. Modify if needed.
        return new Object() {
            public String resume_text = resumeText;
            public String job_description = jobDescription;
        };
    }
}
