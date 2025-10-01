#!/usr/bin/env python3
import re
import json
from bs4 import BeautifulSoup
import html

def extract_questions_from_html(file_path):
    """Extract questions 1-174 from the HTML file with comprehensive details"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    questions = []
    
    # Find all question patterns - looking for <p><strong>number.
    question_patterns = soup.find_all('p')
    
    for i, p_tag in enumerate(question_patterns):
        strong_tag = p_tag.find('strong')
        if not strong_tag:
            continue
            
        strong_text = strong_tag.get_text().strip()
        
        # Check if this starts with a number followed by a period
        question_match = re.match(r'^(\d+)\.\s*(.*)', strong_text)
        if not question_match:
            continue
            
        question_num = int(question_match.group(1))
        
        # Only extract questions 1-174
        if question_num > 174:
            continue
            
        question_text = question_match.group(2)
        
        # Get the complete question text from the strong tag
        complete_question = strong_tag.get_text().strip()
        if complete_question.startswith(f"{question_num}."):
            question_text = complete_question[len(f"{question_num}."):]
        else:
            question_text = complete_question
        
        # Clean up the question text
        question_text = question_text.strip()
        
        print(f"Processing Question {question_num}...")
        
        # Initialize question data
        question_data = {
            "id": question_num,
            "question": question_text,
            "image": None,
            "choices": [],
            "type": "single",  # default
            "correct": [],
            "explanation": ""
        }
        
        # Look for images in the current paragraph or next few elements
        current_element = p_tag
        for _ in range(5):  # Check up to 5 next elements
            if current_element:
                img_tag = current_element.find('img')
                if img_tag and img_tag.get('src'):
                    src = img_tag.get('src')
                    # Convert to relative path format
                    if 'CyberSec_files/' in src:
                        question_data["image"] = src.split('CyberSec_files/')[-1]
                        question_data["image"] = f"CyberSec_files/{question_data['image']}"
                    break
                current_element = current_element.find_next_sibling()
        
        # Find the next <ul> tag which contains the choices
        choices_ul = None
        next_element = p_tag.find_next_sibling()
        
        # Skip any divs or other elements to find the ul
        while next_element and next_element.name != 'ul':
            # Also check for images in intermediate elements
            if not question_data["image"] and next_element.find('img'):
                img_tag = next_element.find('img')
                if img_tag and img_tag.get('src'):
                    src = img_tag.get('src')
                    if 'CyberSec_files/' in src:
                        question_data["image"] = src.split('CyberSec_files/')[-1]
                        question_data["image"] = f"CyberSec_files/{question_data['image']}"
            next_element = next_element.find_next_sibling()
        
        choices_ul = next_element
        
        if choices_ul and choices_ul.name == 'ul':
            choices = []
            correct_indices = []
            
            li_elements = choices_ul.find_all('li')
            
            # Determine if it's multiple choice based on question text
            question_lower = question_text.lower()
            if any(phrase in question_lower for phrase in [
                'choose two', 'choose three', 'choose all', 'select two', 
                'select three', 'select all', 'which two', 'which three',
                'what two', 'what three'
            ]):
                question_data["type"] = "multiple"
            
            for idx, li in enumerate(li_elements):
                choice_text = li.get_text().strip()
                choices.append(choice_text)
                
                # Check if this choice is marked as correct (red color or bold red)
                li_html = str(li)
                
                # Multiple patterns for correct answer detection
                is_correct = False
                
                # Pattern 1: <span style="color: #ff0000;"><strong>text</strong></span>
                if li.find('span', style=lambda x: x and ('color: #ff0000' in x or 'color: red' in x)):
                    is_correct = True
                
                # Pattern 2: <strong><span style="color: #ff0000;">text</span></strong>
                elif li.find('strong') and li.find('span', style=lambda x: x and ('color: #ff0000' in x or 'color: red' in x)):
                    is_correct = True
                
                # Pattern 3: Check raw HTML for red color patterns
                elif ('color: #ff0000' in li_html or 'color: red' in li_html) and ('<strong>' in li_html or '<b>' in li_html):
                    is_correct = True
                
                # Pattern 4: Look for style attributes with red color (hex)
                elif re.search(r'style="[^"]*color:\s*#ff0000[^"]*"', li_html):
                    is_correct = True
                
                # Pattern 5: Look for style attributes with red color (word)  
                elif re.search(r'style="[^"]*color:\s*red[^"]*"', li_html):
                    is_correct = True
                
                # Pattern 6: Check for inline styles with red
                elif re.search(r'style=[\'"][^\'\"]*color:\s*(#ff0000|red)[^\'\"]*[\'"]', li_html):
                    is_correct = True
                
                if is_correct:
                    correct_indices.append(idx)
            
            question_data["choices"] = choices
            question_data["correct"] = correct_indices
        
        # Look for explanation - usually in a div with class containing "message" or after the choices
        explanation_element = None
        if choices_ul:
            explanation_element = choices_ul.find_next_sibling()
            
        # Check several next elements for explanation
        check_element = explanation_element
        for _ in range(10):
            if check_element:
                if check_element.name == 'div' and ('message' in str(check_element.get('class', [])) or 
                                                   'explanation' in check_element.get_text().lower()):
                    explanation_text = check_element.get_text().strip()
                    # Clean up explanation text
                    if explanation_text.startswith('Explanation:'):
                        explanation_text = explanation_text.replace('Explanation:', '').strip()
                    question_data["explanation"] = explanation_text
                    break
                elif 'explanation' in check_element.get_text().lower()[:50]:
                    explanation_text = check_element.get_text().strip()
                    if explanation_text.startswith('Explanation:'):
                        explanation_text = explanation_text.replace('Explanation:', '').strip()
                    question_data["explanation"] = explanation_text
                    break
                check_element = check_element.find_next_sibling()
            else:
                break
        
        questions.append(question_data)
    
    # Sort questions by ID to ensure proper order
    questions.sort(key=lambda x: x["id"])
    
    return {"questions": questions}

if __name__ == "__main__":
    file_path = "/home/christopher/Downloads/CyberSec.html"
    
    print("Extracting questions from CyberSec.html...")
    result = extract_questions_from_html(file_path)
    
    output_file = "/home/christopher/Downloads/questions_fixed.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Extracted {len(result['questions'])} questions")
    print(f"Questions saved to {output_file}")
    
    # Print summary
    single_count = sum(1 for q in result['questions'] if q['type'] == 'single')
    multiple_count = sum(1 for q in result['questions'] if q['type'] == 'multiple')
    with_images = sum(1 for q in result['questions'] if q['image'])
    with_explanations = sum(1 for q in result['questions'] if q['explanation'])
    
    print(f"\nSummary:")
    print(f"- Single choice questions: {single_count}")
    print(f"- Multiple choice questions: {multiple_count}")
    print(f"- Questions with images: {with_images}")
    print(f"- Questions with explanations: {with_explanations}")