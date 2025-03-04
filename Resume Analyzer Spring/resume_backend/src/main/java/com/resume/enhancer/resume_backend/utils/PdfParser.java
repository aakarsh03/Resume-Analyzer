package com.resume.enhancer.resume_backend.utils;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;
import org.springframework.web.multipart.MultipartFile;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.io.InputStream;

public class PdfParser {

    private static final Logger logger = LoggerFactory.getLogger(PdfParser.class);

    /**
     * Extracts text from the provided PDF file.
     *
     * @param file the PDF file to extract text from
     * @return extracted text as a String
     * @throws IOException if an error occurs while processing the PDF
     */
    public static String extractText(MultipartFile file) throws IOException {
        // Validate the file is not empty
        if (file.isEmpty()) {
            logger.error("Received an empty file.");
            throw new IllegalArgumentException("File is empty.");
        }

        // Open the PDF document and extract the text
        try (InputStream inputStream = file.getInputStream();
             PDDocument document = PDDocument.load(inputStream)) {

            // Check if the document is encrypted
            if (document.isEncrypted()) {
                logger.error("The PDF is encrypted and cannot be processed.");
                throw new IOException("The PDF is encrypted and cannot be processed.");
            }

            // Extract text using PDFTextStripper
            String extractedText = new PDFTextStripper().getText(document);

            // Log the length of the extracted text for debugging, but avoid printing it directly
            logger.info("Successfully extracted text from the PDF. Extracted text length: {}", extractedText.length());

            return extractedText;

        } catch (IOException e) {
            // Log the error and rethrow it with more context
            logger.error("Error processing PDF file", e);
            throw new IOException("Error processing PDF file: " + e.getMessage(), e);
        }
    }
}
