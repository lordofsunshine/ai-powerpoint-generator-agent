import json
import time
import aiohttp
import asyncio
import warnings
from typing import Optional
from ..localization.manager import get_localization_manager

warnings.filterwarnings('ignore', category=UnicodeWarning)


class IoNetService:
    def __init__(self, api_key: str, model: str = "meta-llama/Llama-3.3-70B-Instruct"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.intelligence.io.solutions/api/v1"
        self.max_attempts = 3
        self.retry_delay = 1.0
        self.loc = get_localization_manager()
        
    async def _make_request(self, messages: list, temperature: float = 0.7) -> Optional[str]:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_completion_tokens": 800,
            "stream": False
        }
        
        for attempt in range(self.max_attempts):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f"{self.base_url}/chat/completions",
                        headers=headers,
                        json=data,
                        timeout=30
                    ) as response:
                        if response.status == 401:
                            try:
                                error_text = await response.text()
                            except:
                                error_text = self.loc.t("error_invalid_api_key")
                            raise Exception(f"{self.loc.t('error_invalid_api_key')} (401): {error_text}")
                        elif response.status == 429:
                            if attempt < self.max_attempts - 1:
                                await asyncio.sleep(self.retry_delay * (attempt + 1) * 2)
                                continue
                            raise Exception(self.loc.t("error_rate_limit"))
                        elif response.status == 400:
                            try:
                                error_data = await response.json()
                                error_detail = error_data.get("detail", "")
                                if "does not support Chat Completions API" in error_detail:
                                    supported_models = error_data.get("Supported models", [])
                                    if supported_models:
                                        models_list = ", ".join(supported_models[:5])
                                        error_msg = f"{self.loc.t('error_model_not_supported')}. {self.loc.t('error_model_suggestion')}. {self.loc.t('error_supported_models')}: {models_list}..."
                                    else:
                                        error_msg = f"{self.loc.t('error_model_not_supported')}. {self.loc.t('error_switch_model')}."
                                    raise Exception(error_msg)
                                else:
                                    raise Exception(f"API error 400: {error_detail}")
                            except json.JSONDecodeError:
                                error_text = await response.text()
                                raise Exception(f"API error 400: {error_text}")
                        elif response.status != 200:
                            try:
                                error_text = await response.text()
                            except:
                                error_text = f"HTTP {response.status}"
                            raise Exception(f"{self.loc.t('error_api_error')} {response.status}: {error_text}")
                        
                        result = await response.json()
                        content = result["choices"][0]["message"]["content"]
                        if isinstance(content, str):
                            try:
                                return content.strip()
                            except UnicodeDecodeError:
                                return content.encode('utf-8', errors='ignore').decode('utf-8').strip()
                        return str(content).strip()
                
            except Exception as e:
                if attempt < self.max_attempts - 1:
                    await asyncio.sleep(self.retry_delay * (attempt + 1))
                    continue
                if "Invalid API key" in str(e) or "401" in str(e):
                    raise Exception(self.loc.t("error_invalid_api_key"))
                elif "Rate limit" in str(e) or "429" in str(e):
                    raise Exception(self.loc.t("error_rate_limit"))
                elif "API error" in str(e):
                    raise e
                else:
                    raise Exception(f"{self.loc.t('error_network')}: {str(e)}")
                
        return None
    
    async def test_api_key(self) -> bool:
        try:
            test_messages = [{"role": "user", "content": "Если видишь это сообщение, то напиши в JSON формате: {\"success\": true}"}]
            response = await self._make_request(test_messages, temperature=0.1)
            if response:
                try:
                    import json
                    result = json.loads(response)
                    return result.get("success", False)
                except:
                    return "success" in response.lower() and "true" in response.lower()
            return False
        except Exception as e:
            if self.loc.t("error_invalid_api_key") in str(e) or "401" in str(e):
                return False
            return False
    
    async def generate_response(self, prompt: str, temperature: float = 0.7) -> Optional[str]:
        messages = [{"role": "user", "content": prompt}]
        return await self._make_request(messages, temperature)
    
    def parse_json_response(self, response_text: str) -> Optional[dict]:
        try:
            cleaned_response = response_text.replace('\n', '').replace('\r', '')
            return json.loads(cleaned_response)
        except json.JSONDecodeError:
            try:
                start_idx = cleaned_response.find('{')
                end_idx = cleaned_response.rfind('}') + 1
                if start_idx != -1 and end_idx != 0:
                    json_part = cleaned_response[start_idx:end_idx]
                    return json.loads(json_part)
            except json.JSONDecodeError:
                pass
        return None
