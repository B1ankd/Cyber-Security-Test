# CyberSec.html Question Extraction Report

## Summary
- **Target**: Extract questions 1-174 from CyberSec.html
- **Total Extracted**: 147 questions 
- **Missing**: 27 questions
- **Success Rate**: 84.5%

## Extracted Question Statistics
- **Single Choice Questions**: 123
- **Multiple Choice Questions**: 26
- **Questions with Images**: 74 (50.3%)
- **Questions with Explanations**: 136 (92.5%)
- **Questions with Correct Answers Detected**: 146 (99.3%)

## Missing Questions (1-174)
The following question numbers were not found or extracted:
22, 46, 52, 116-126, 132, 134-135, 137, 143-145, 148-150, 164-165, 167

Note: Some of these questions (like 46, 52) exist in the HTML but have different formatting that wasn't captured by the extraction patterns.

## Question Format Structure
```json
{
  "id": 1,
  "question": "question text",
  "image": "CyberSec_files/image.png" or null,
  "choices": ["choice1", "choice2", "choice3", "choice4"],
  "type": "single" or "multiple",
  "correct": [0] for single choice or [0,2] for multiple choice,
  "explanation": "explanation text"
}
```

## Features Successfully Extracted

### 1. Question Types
- ✅ Single choice (radio button) questions
- ✅ Multiple choice (checkbox) questions identified by phrases like "Choose two", "Choose three", etc.

### 2. Images
- ✅ Images detected and converted to relative paths (CyberSec_files/filename)
- ✅ Images found in question context or exhibits

### 3. Answer Choices
- ✅ All answer choices extracted (some questions have 5+ choices)
- ✅ Complete choice text preserved

### 4. Correct Answers
- ✅ Detected red-colored text (both #ff0000 and "red")
- ✅ Detected bold red combinations
- ✅ Multiple detection patterns for different HTML structures

### 5. Explanations
- ✅ Explanation text extracted from following div elements
- ✅ "Explanation:" prefix removed for cleaner text

## Sample Multiple Choice Questions
- Question 26: "Which two VTP modes..." (correct answers: 4, 5)
- Question 27: "Which three steps..." (correct answers: 0, 4, 5) 
- Question 29: "All the displayed switches..." (correct answers: 1, 2, 4)

## Output File
Questions saved to: `/home/christopher/Downloads/questions_fixed.json`

## Recommendations for Missing Questions
The 27 missing questions may have:
- Different HTML formatting that doesn't match the extraction patterns
- Been marked as missing in the original document
- Different numbering schemes
- Non-standard structures

To capture these, manual review of the HTML around the missing question numbers would be needed to identify alternative patterns.