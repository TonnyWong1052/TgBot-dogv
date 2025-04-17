import logging
from openai import OpenAI
from ..llm_client import LLMProvider

logger = logging.getLogger("github_provider")

class GitHubProvider(LLMProvider):
    """
    GitHub (via Azure) API 的提供商實現
    """
    def __init__(self, api_key=None):
        """
        初始化 GitHub 提供商
        
        Args:
            api_key (str, optional): GitHub API 密鑰
        """
        super().__init__(api_key)
        self.endpoint = "https://models.inference.ai.azure.com"
        if not self.api_key:
            logger.warning("GitHub API key is not provided")
    
    def call(self, prompt, **kwargs):
        """
        調用 GitHub API 生成響應
        
        Args:
            prompt (str): 用戶提示
            **kwargs: 附加參數，包括:
                system_prompt (str): 設置上下文的系統提示
                model_name (str): 要使用的模型 (默認: gpt-4o-mini)
                
        Returns:
            str: 生成的文本響應
        """
        system_prompt = kwargs.get('system_prompt', 'You are a helpful AI assistant.')
        model_name = kwargs.get('model_name', 'gpt-4o-mini')
        
        if not self.api_key:
            return "GitHub API key not found. Please set it in the .env file or credentials file."
        
        try:
            client = OpenAI(
                base_url=self.endpoint,
                api_key=self.api_key,
            )

            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=1.0,
                top_p=1.0,
                max_tokens=1000,
                model=model_name
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error calling GitHub API: {e}")
            return f"Error calling GitHub API: {str(e)}"
    
    def call_stream(self, prompt, **kwargs):
        """
        使用流式支持調用 GitHub API 生成響應
        
        Args:
            prompt (str): 用戶提示
            **kwargs: 附加參數，包括:
                system_prompt (str): 設置上下文的系統提示
                model_name (str): 要使用的模型 (默認: gpt-4o-mini)
                
        Returns:
            Generator: 生成部分響應的生成器
        """
        system_prompt = kwargs.get('system_prompt', 'You are a helpful AI assistant.')
        model_name = kwargs.get('model_name', 'gpt-4o-mini')
        
        if not self.api_key:
            yield "GitHub API key not found. Please set it in the .env file or credentials file."
            return
        
        try:
            client = OpenAI(
                base_url=self.endpoint,
                api_key=self.api_key,
            )

            stream = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=1.0,
                top_p=1.0,
                max_tokens=1000,
                model=model_name,
                stream=True
            )
            
            full_response = ""
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    yield full_response
                    
        except Exception as e:
            logger.error(f"Error streaming from GitHub API: {e}")
            yield f"Error streaming from GitHub API: {str(e)}" 