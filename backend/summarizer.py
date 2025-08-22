import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict, List
import json

load_dotenv()

class PaperSummarizer:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )
    
    def _truncate_text(self, text: str, max_tokens: int = 3000) -> str:
        """Truncate text to fit within token limits."""
        # Rough estimation: 1 token ≈ 4 characters
        max_chars = max_tokens * 4
        if len(text) <= max_chars:
            return text
        
        # Try to truncate at paragraph boundary
        truncated = text[:max_chars]
        last_paragraph = truncated.rfind('\n\n')
        if last_paragraph > max_chars // 2:
            return truncated[:last_paragraph]
        
        return truncated
    
    def generate_summary(self, text: str) -> Dict:
        """Generate summary, pros/cons, and future work for a research paper."""
        # Truncate text if too long
        truncated_text = self._truncate_text(text)
        
        try:
            # Generate summary
            summary = self._generate_summary(truncated_text)
            
            # Generate pros and cons
            pros_cons = self._generate_pros_cons(truncated_text)
            
            # Generate future work
            future_work = self._generate_future_work(truncated_text)
            
            return {
                "summary": summary,
                "pros": pros_cons.get("pros", []),
                "cons": pros_cons.get("cons", []),
                "future_work": future_work
            }
            
        except Exception as e:
            return {
                "summary": f"Error generating summary: {str(e)}",
                "pros": [],
                "cons": [],
                "future_work": []
            }
    
    def _generate_summary(self, text: str) -> str:
        """Generate a comprehensive summary of the paper."""
        prompt = f"""Please provide a comprehensive summary of this research paper. Include:
1. The main research question or problem addressed
2. The methodology used
3. Key findings and results
4. Main contributions to the field

Paper content:
{text}

Summary:"""

        try:
            completion = self.client.chat.completions.create(
                model="openai/gpt-oss-20b:free",
                messages=[{"role": "user", "content": prompt}],
                extra_headers={
                    "HTTP-Referer": "http://localhost:3000",
                    "X-Title": "ResearchRAG",
                }
            )
            
            return completion.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def _generate_pros_cons(self, text: str) -> Dict[str, List[str]]:
        """Generate pros and cons of the research paper."""
        prompt = f"""Analyze this research paper and provide:
1. Strengths/Pros (3-5 points)
2. Weaknesses/Cons (3-5 points)

Please format your response as JSON with "pros" and "cons" arrays.

Paper content:
{text}

Analysis:"""

        try:
            completion = self.client.chat.completions.create(
                model="openai/gpt-oss-20b:free",
                messages=[{"role": "user", "content": prompt}],
                extra_headers={
                    "HTTP-Referer": "http://localhost:3000",
                    "X-Title": "ResearchRAG",
                }
            )
            
            response = completion.choices[0].message.content.strip()
            
            # Try to parse as JSON
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                # If JSON parsing fails, extract manually
                return self._extract_pros_cons_from_text(response)
                
        except Exception as e:
            return {"pros": [f"Error generating pros/cons: {str(e)}"], "cons": []}
    
    def _extract_pros_cons_from_text(self, text: str) -> Dict[str, List[str]]:
        """Extract pros and cons from unstructured text."""
        lines = text.split('\n')
        pros = []
        cons = []
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check for section headers
            if any(word in line.lower() for word in ['pros', 'strengths', 'advantages']):
                current_section = 'pros'
                continue
            elif any(word in line.lower() for word in ['cons', 'weaknesses', 'disadvantages']):
                current_section = 'cons'
                continue
            
            # Extract bullet points
            if line.startswith(('-', '•', '*', '1.', '2.', '3.', '4.', '5.')):
                point = line.lstrip('-•*123456789. ').strip()
                if current_section == 'pros':
                    pros.append(point)
                elif current_section == 'cons':
                    cons.append(point)
        
        # If no structured format found, provide default
        if not pros and not cons:
            pros = ["Analysis could not be properly extracted"]
            cons = ["Analysis could not be properly extracted"]
        
        return {"pros": pros, "cons": cons}
    
    def _generate_future_work(self, text: str) -> List[str]:
        """Generate future work suggestions based on the paper."""
        prompt = f"""Based on this research paper, suggest 3-5 areas for future work or research directions. 
Please provide specific, actionable suggestions that build upon this work.

Format your response as a simple list with each suggestion on a new line starting with "- ".

Paper content:
{text}

Future work suggestions:"""

        try:
            completion = self.client.chat.completions.create(
                model="openai/gpt-oss-20b:free",
                messages=[{"role": "user", "content": prompt}],
                extra_headers={
                    "HTTP-Referer": "http://localhost:3000",
                    "X-Title": "ResearchRAG",
                }
            )
            
            response = completion.choices[0].message.content.strip()
            
            # Extract list items
            future_work = []
            for line in response.split('\n'):
                line = line.strip()
                if line.startswith('-'):
                    future_work.append(line[1:].strip())
                elif line and not any(word in line.lower() for word in ['future', 'work', 'suggestions']):
                    # If it's not a header, treat as a suggestion
                    future_work.append(line)
            
            return future_work[:5]  # Limit to 5 suggestions
            
        except Exception as e:
            return [f"Error generating future work: {str(e)}"]
