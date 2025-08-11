"""
AI Service for content generation using OpenAI, Anthropic, or Ollama
"""

import requests
import openai
from anthropic import Anthropic
from typing import Optional
from config import config
from utils.logger import get_logger

logger = get_logger(__name__)

class AIService:
    """Handle AI-powered content generation with automatic provider selection"""
    
    def __init__(self, provider: Optional[str] = None):
        self.provider = provider or config.default_ai_provider
        self._setup_clients()
    
    def _setup_clients(self) -> None:
        """Initialize AI clients based on available providers"""
        try:
            if self.provider == 'openai' and config.openai_api_key:
                openai.api_key = config.openai_api_key
                logger.info("OpenAI client configured")
                
            elif self.provider == 'anthropic' and config.anthropic_api_key:
                self.anthropic_client = Anthropic(api_key=config.anthropic_api_key)
                logger.info("Anthropic client configured")
                
            elif self.provider == 'ollama':
                try:
                    # Test connection to Ollama
                    test_response = requests.get(f"{config.ollama_base_url}/api/tags", timeout=5)
                    if test_response.status_code == 200:
                        models = test_response.json().get('models', [])
                        model_names = [model.get('name', '') for model in models]
                        
                        if config.ollama_model in model_names:
                            logger.info(f"Ollama configured with model {config.ollama_model} at {config.ollama_base_url}")
                        else:
                            logger.warning(f"Ollama model {config.ollama_model} not found. Available models: {model_names}")
                            if model_names:
                                logger.info(f"You can pull the model with: ollama pull {config.ollama_model}")
                    else:
                        logger.warning(f"Ollama server not responding at {config.ollama_base_url}")
                except requests.exceptions.ConnectionError:
                    logger.warning(f"Cannot connect to Ollama at {config.ollama_base_url}. Make sure Ollama is installed and running.")
                except Exception as e:
                    logger.warning(f"Ollama setup check failed: {e}")
                
        except Exception as e:
            logger.error(f"Failed to setup AI client: {e}")
    
    def generate_content(self, prompt: str, content_type: str = "article", 
                        provider: Optional[str] = None) -> str:
        """
        Generate content using the configured AI provider
        
        Args:
            prompt: Content prompt/topic
            content_type: Type of content (article, blog, page, etc.)
            provider: Override default provider
            
        Returns:
            Generated content string
        """
        selected_provider = provider or self.provider
        
        try:
            if selected_provider == 'openai' and config.openai_api_key:
                return self._generate_openai(prompt, content_type)
                
            elif selected_provider == 'anthropic' and config.anthropic_api_key:
                return self._generate_anthropic(prompt, content_type)
                
            elif selected_provider == 'ollama':
                return self._generate_ollama(prompt, content_type)
                
            else:
                return f"AI provider '{selected_provider}' not configured or unavailable"
                
        except Exception as e:
            logger.error(f"AI content generation failed: {e}")
            return f"Error generating content: {str(e)}"
    
    def _generate_openai(self, prompt: str, content_type: str) -> str:
        """Generate content using OpenAI"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": f"Generate a {content_type} for a Drupal website. Format with HTML tags appropriate for Drupal content."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500
        )
        return response.choices[0].message.content
    
    def _generate_anthropic(self, prompt: str, content_type: str) -> str:
        """Generate content using Anthropic Claude"""
        message = self.anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1500,
            messages=[
                {
                    "role": "user", 
                    "content": f"Generate a {content_type} for a Drupal website about: {prompt}. Format with HTML tags appropriate for Drupal content."
                }
            ]
        )
        return message.content[0].text
    
    def _generate_ollama(self, prompt: str, content_type: str) -> str:
        """Generate content using Ollama with local small language model"""
        try:
            # Check if Ollama is running
            health_response = requests.get(f"{config.ollama_base_url}/api/tags", timeout=5)
            if health_response.status_code != 200:
                return "Ollama server is not running. Please start Ollama first."
            
            # Use the configured model (default: llama3.2:1b for efficiency)
            model_name = config.ollama_model
            
            # Optimized prompt for better local model performance
            system_prompt = f"You are a helpful assistant that creates {content_type} content for Drupal websites. Keep responses concise and well-formatted."
            full_prompt = f"{system_prompt}\n\nTopic: {prompt}\n\nGenerate a {content_type} about this topic. Use simple HTML tags like <p>, <h2>, <ul>, <li> for formatting:"
            
            response = requests.post(
                f"{config.ollama_base_url}/api/generate",
                json={
                    "model": model_name,
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_k": 40,
                        "top_p": 0.9,
                        "num_predict": 1000  # Limit response length for efficiency
                    }
                },
                timeout=config.ollama_timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("response", "No content generated")
                
                # Clean up the content if needed
                if content.strip():
                    return content.strip()
                else:
                    return "No content was generated. Please try again."
            else:
                return f"Ollama API error: {response.status_code} - {response.text}"
                
        except requests.exceptions.Timeout:
            return f"Ollama request timed out after {config.ollama_timeout} seconds. The model might be loading or processing."
        except requests.exceptions.ConnectionError:
            return "Cannot connect to Ollama. Please ensure Ollama is installed and running on http://localhost:11434"
        except Exception as e:
            return f"Ollama error: {str(e)}"
    
    def suggest_taxonomy_terms(self, content: str, vocabulary: str = "tags") -> list:
        """
        Suggest taxonomy terms for content
        
        Args:
            content: Content to analyze
            vocabulary: Target vocabulary name
            
        Returns:
            List of suggested terms
        """
        try:
            prompt = f"Suggest 5-10 relevant {vocabulary} for this content: {content[:500]}..."
            
            if self.provider == 'openai' and config.openai_api_key:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Return only a comma-separated list of tags/terms."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=100
                )
                terms_text = response.choices[0].message.content
                return [term.strip() for term in terms_text.split(',')]
                
        except Exception as e:
            logger.error(f"Taxonomy suggestion failed: {e}")
            
        return []
    
    def summarize_content(self, content: str, max_length: int = 200) -> str:
        """
        Summarize node content
        
        Args:
            content: Content to summarize
            max_length: Maximum summary length
            
        Returns:
            Content summary
        """
        try:
            prompt = f"Summarize this content in {max_length} characters or less: {content}"
            
            if self.provider == 'openai' and config.openai_api_key:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": f"Provide a concise summary in {max_length} characters or less."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=100
                )
                return response.choices[0].message.content
                
        except Exception as e:
            logger.error(f"Content summarization failed: {e}")
            
        return content[:max_length] + "..." if len(content) > max_length else content
