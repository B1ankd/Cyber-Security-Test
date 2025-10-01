#!/usr/bin/env python3
import re
import json

def extract_questions(html_content):
    """Extract all questions from the HTML content"""
    questions = []
    
    # Split content by question pattern
    # Look for patterns like <strong>NUMBER. or <p><strong>NUMBER. or <b>NUMBER.
    question_pattern = re.compile(r'(<p>)?<(?:strong|b)>(\d{1,3})\.\s*(.+?)(?=(?:<p>)?<(?:strong|b)>\d{1,3}\.|$)', re.DOTALL)
    
    matches = question_pattern.findall(html_content)
    
    for match in matches:
        question_num = int(match[1])
        
        # Skip if it's not in the range we're looking for
        if question_num > 174:
            continue
            
        full_content = match[2]
        
        # Extract question text (up to the first </strong> or </b> or <ul> or <pre>)
        question_match = re.search(r'^(.+?)(?:</strong>|</b>|<ul>|<pre>)', full_content, re.DOTALL)
        if question_match:
            question_text = question_match.group(1)
        else:
            # If no clear end, take up to first newline or 500 chars
            question_text = full_content.split('\n')[0][:500]
        
        # Clean question text
        question_text = re.sub(r'<[^>]+>', '', question_text)
        question_text = re.sub(r'\s+', ' ', question_text).strip()
        
        # Extract choices
        choices = []
        correct_index = -1
        
        # Look for <ul> section
        ul_match = re.search(r'<ul>(.*?)</ul>', full_content, re.DOTALL)
        if ul_match:
            ul_content = ul_match.group(1)
            li_pattern = re.compile(r'<li>(.*?)</li>', re.DOTALL)
            
            for idx, li_match in enumerate(li_pattern.findall(ul_content)):
                choice_text = li_match
                # Check if this is the correct answer
                if 'color: red' in choice_text or 'color: #ff0000' in choice_text or 'color: #FF0000' in choice_text:
                    correct_index = idx
                
                # Clean choice text
                choice_text = re.sub(r'<[^>]+>', '', choice_text)
                choice_text = re.sub(r'\s+', ' ', choice_text).strip()
                
                if choice_text:
                    choices.append(choice_text)
        
        # Look for <pre> section if no <ul> found
        if not choices:
            pre_match = re.search(r'<pre>(.*?)</pre>', full_content, re.DOTALL)
            if pre_match:
                pre_content = pre_match.group(1)
                lines = pre_content.split('\n')
                
                for idx, line in enumerate(lines):
                    if line.strip():
                        # Check if this is marked as correct
                        if 'correct_answer' in line or 'color: red' in line:
                            correct_index = idx
                        
                        # Clean line
                        clean_line = re.sub(r'<[^>]+>', '', line).strip()
                        if clean_line and not clean_line.startswith('<'):
                            choices.append(clean_line)
        
        # Extract explanation
        explanation = ""
        explanation_match = re.search(r'message_box success[^>]*>(.*?)(?:</div>|$)', full_content, re.DOTALL)
        if explanation_match:
            explanation = explanation_match.group(1)
            # Clean explanation
            explanation = re.sub(r'<[^>]+>', '', explanation)
            explanation = re.sub(r'Explanation:\s*', '', explanation, flags=re.IGNORECASE)
            explanation = re.sub(r'Explain:\s*', '', explanation, flags=re.IGNORECASE)
            explanation = re.sub(r'\s+', ' ', explanation).strip()
        
        # Create question object
        question = {
            'id': question_num,
            'question': question_text,
            'choices': choices,
            'correct': correct_index,
            'explanation': explanation
        }
        
        questions.append(question)
    
    return questions

def main():
    # Read the HTML file
    with open('/home/christopher/Downloads/CyberSec.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract questions
    questions = extract_questions(content)
    
    # Remove duplicates and sort
    seen_ids = set()
    unique_questions = []
    for q in questions:
        if q['id'] not in seen_ids:
            seen_ids.add(q['id'])
            unique_questions.append(q)
    
    questions = sorted(unique_questions, key=lambda x: x['id'])
    
    # Create the final JSON structure
    output = {
        'questions': questions
    }
    
    # Save to file
    with open('/home/christopher/Downloads/extracted_questions.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"Extracted {len(questions)} questions")
    
    # Print summary
    question_ids = [q['id'] for q in questions]
    print(f"Question IDs range: {min(question_ids)} to {max(question_ids)}")
    
    # Check for missing questions up to 174
    expected_ids = set(range(1, 175))
    found_ids = set(question_ids)
    missing_ids = expected_ids - found_ids
    
    if missing_ids:
        print(f"Missing {len(missing_ids)} question IDs: {sorted(missing_ids)}")
    else:
        print("All questions 1-174 were found!")
    
    # Print sample of extracted questions
    print("\nSample of extracted questions:")
    for q in questions[:3]:
        print(f"\nQuestion {q['id']}: {q['question'][:80]}...")
        print(f"Choices: {len(q['choices'])}")
        print(f"Correct answer index: {q['correct']}")
        print(f"Has explanation: {'Yes' if q['explanation'] else 'No'}")

if __name__ == "__main__":
    main()