from typing import AsyncIterator
from dashscope import Generation
from app.config import settings
import dashscope


class LLMService:
    """阿里百炼 LLM 服务"""

    def __init__(self):
        dashscope.api_key = settings.DASHSCOPE_API_KEY
        self.model = settings.LLM_MODEL

    async def generate(self, prompt: str) -> str:
        """生成回答（非流式）"""
        response = Generation.call(
            model=self.model,
            prompt=prompt,
            temperature=settings.LLM_TEMPERATURE
        )

        if response.status_code == 200:
            return response.output.text
        else:
            raise Exception(f"LLM API error: {response.message}")

    async def generate_stream(self, prompt: str) -> AsyncIterator[str]:
        """流式生成回答"""
        try:
            responses = Generation.call(
                model=self.model,
                prompt=prompt,
                temperature=settings.LLM_TEMPERATURE,
                stream=True,
                incremental_output=True
            )

            for response in responses:
                if response.status_code == 200:
                    # 获取增量输出
                    text = response.output.text
                    if text:
                        yield text
                else:
                    print(f"Stream error: {response.message}")
                    break

        except Exception as e:
            print(f"Stream generation error: {e}")
            # 如果流式失败，尝试非流式
            try:
                full_response = await self.generate(prompt)
                yield full_response
            except:
                pass


# 全局单例
llm_service = LLMService()
