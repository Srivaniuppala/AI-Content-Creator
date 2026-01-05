"""
Groq API Integration Service
Handles communication with Groq for content generation
"""

import os
import requests
from typing import Dict, List, Optional, Generator
import json

class OllamaService:
    def __init__(self):
        """Initialize Groq service"""
        self.api_key = os.getenv("GROQ_API_KEY", "")
        self.base_url = "https://api.groq.com/openai/v1"
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.api_chat = f"{self.base_url}/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def check_connection(self) -> bool:
        """Check if Groq API key is valid"""
        if not self.api_key:
            return False
        try:
            response = requests.post(
                self.api_chat,
                headers=self.headers,
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": "test"}],
                    "max_tokens": 5
                },
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
    
    def list_models(self) -> List[str]:
        """List available models in Groq"""
        return [
            "llama-3.3-70b-versatile",
            "llama-3.1-70b-versatile",
            "mixtral-8x7b-32768",
            "gemma2-9b-it"
        ]
    
    def generate_content(self, prompt: str, system_prompt: str = None, 
                        stream: bool = False) -> Optional[str]:
        """
        Generate content using Groq API
        
        Args:
            prompt: User prompt
            system_prompt: System instructions
            stream: Whether to stream the response
            
        Returns:
            Generated text or None if error
        """
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": stream
            }
            
            response = requests.post(
                self.api_chat,
                headers=self.headers,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                if stream:
                    return response.text
                else:
                    data = response.json()
                    return data['choices'][0]['message']['content']
            return None
            
        except Exception as e:
            print(f"Error generating content: {e}")
            return None
    
    def generate_content_stream(self, prompt: str, system_prompt: str = None) -> Generator:
        """
        Generate content with streaming response
        
        Args:
            prompt: User prompt
            system_prompt: System instructions
            
        Yields:
            Chunks of generated text
        """
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": True
            }
            
            response = requests.post(
                self.api_chat,
                headers=self.headers,
                json=payload,
                stream=True,
                timeout=120
            )
            
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        try:
                            line_text = line.decode('utf-8')
                            if line_text.startswith('data: '):
                                line_text = line_text[6:]
                            if line_text.strip() == '[DONE]':
                                break
                            data = json.loads(line_text)
                            if 'choices' in data and len(data['choices']) > 0:
                                delta = data['choices'][0].get('delta', {})
                                if 'content' in delta:
                                    yield delta['content']
                        except json.JSONDecodeError:
                            continue
                            
        except Exception as e:
            print(f"Error in streaming: {e}")
            yield f"Error: {str(e)}"
    
    def chat_completion(self, messages: List[Dict[str, str]], stream: bool = False) -> Optional[str]:
        """
        Generate chat completion
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            stream: Whether to stream the response
            
        Returns:
            Generated response or None if error
        """
        try:
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": stream
            }
            
            response = requests.post(
                self.api_chat,
                headers=self.headers,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                if stream:
                    return response.text
                else:
                    data = response.json()
                    return data['choices'][0]['message']['content']
            return None
            
        except Exception as e:
            print(f"Error in chat completion: {e}")
            return None
    
    def chat_completion_stream(self, messages: List[Dict[str, str]]) -> Generator:
        """
        Generate chat completion with streaming
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            
        Yields:
            Chunks of generated text
        """
        try:
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": True
            }
            
            response = requests.post(
                self.api_chat,
                headers=self.headers,
                json=payload,
                stream=True,
                timeout=120
            )
            
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        try:
                            line_text = line.decode('utf-8')
                            if line_text.startswith('data: '):
                                line_text = line_text[6:]
                            if line_text.strip() == '[DONE]':
                                break
                            data = json.loads(line_text)
                            if 'choices' in data and len(data['choices']) > 0:
                                delta = data['choices'][0].get('delta', {})
                                if 'content' in delta:
                                    yield delta['content']
                        except json.JSONDecodeError:
                            continue
                            
        except Exception as e:
            print(f"Error in streaming chat: {e}")
            yield f"Error: {str(e)}"
    
    def create_content_prompt(self, content_type: str, user_prompt: str, 
                             tone: str = "professional", length: str = "medium") -> str:
        """
        Create optimized prompt based on content type
        
        Args:
            content_type: Type of content to generate
            user_prompt: User's input prompt
            tone: Desired tone
            length: Desired length
            
        Returns:
            Formatted prompt for LLM
        """
        length_guidelines = {
            "short": "Keep it concise, around 50-100 words.",
            "medium": "Make it moderate length, around 150-250 words.",
            "long": "Create detailed content, around 300-500 words."
        }
        
        tone_guidelines = {
            "professional": "Use professional, formal language.",
            "casual": "Use casual, friendly language.",
            "creative": "Be creative and engaging.",
            "persuasive": "Be persuasive and compelling.",
            "informative": "Be informative and educational."
        }
        
        prompts = {
            "LinkedIn Post": f"""Create a professional LinkedIn post about: {user_prompt}

Requirements:
- {tone_guidelines.get(tone, tone_guidelines['professional'])}
- {length_guidelines.get(length, length_guidelines['medium'])}
- Include relevant hashtags
- Make it engaging and valuable for LinkedIn audience
- Use appropriate formatting with line breaks

Generate only the post content, no explanations.""",
            
            "Professional Email": f"""Write a professional email about: {user_prompt}

Requirements:
- {tone_guidelines.get(tone, tone_guidelines['professional'])}
- Include appropriate subject line
- Proper email structure (greeting, body, closing)
- {length_guidelines.get(length, length_guidelines['medium'])}
- Clear and concise communication

Generate only the email content.""",
            
            "Ad Content": f"""Create compelling ad copy for: {user_prompt}

Requirements:
- {tone_guidelines.get(tone, tone_guidelines['persuasive'])}
- {length_guidelines.get(length, length_guidelines['short'])}
- Include attention-grabbing headline
- Focus on benefits and call-to-action
- Persuasive and engaging

Generate only the ad content.""",
            
            "Conversational Text": f"""Generate conversational text about: {user_prompt}

Requirements:
- {tone_guidelines.get(tone, tone_guidelines['casual'])}
- {length_guidelines.get(length, length_guidelines['medium'])}
- Natural, flowing conversation style
- Engaging and relatable

Generate only the conversational text.""",
            
            "Blog Post": f"""Write a blog post about: {user_prompt}

Requirements:
- {tone_guidelines.get(tone, tone_guidelines['informative'])}
- {length_guidelines.get(length, length_guidelines['long'])}
- Include engaging title
- Well-structured with introduction, body, conclusion
- Informative and valuable content

Generate only the blog post.""",
            
            "Social Media Caption": f"""Create a social media caption for: {user_prompt}

Requirements:
- {tone_guidelines.get(tone, tone_guidelines['casual'])}
- {length_guidelines.get(length, length_guidelines['short'])}
- Engaging and shareable
- Include relevant hashtags and emojis
- Platform-appropriate

Generate only the caption."""
        }
        
        return prompts.get(content_type, f"Generate {content_type} content about: {user_prompt}")
