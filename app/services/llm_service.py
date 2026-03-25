import json
import logging
import re
from typing import AsyncGenerator
import anthropic
from app.core.config import settings

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = settings.LLM_MODEL
        self.max_tokens = settings.LLM_MAX_TOKENS
        self.temperature = settings.LLM_TEMPERATURE

    def generate(self, system: str, user_prompt: str) -> tuple:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=system,
            messages=[{"role": "user", "content": user_prompt}],
        )
        content = response.content[0].text
        parsed = self._parse_json(content)
        usage = {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        }
        return parsed, usage

    def generate_stream(self, system: str, user_prompt: str):
        with self.client.messages.stream(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=system,
            messages=[{"role": "user", "content": user_prompt}],
        ) as stream:
            for text in stream.text_stream:
                yield text

    def generate_chat(self, system: str, messages: list):
        formatted = [{"role": m["role"], "content": m["content"]} for m in messages]
        with self.client.messages.stream(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=0.4,
            system=system,
            messages=formatted,
        ) as stream:
            for text in stream.text_stream:
                yield text

    @staticmethod
    def _parse_json(text: str) -> dict:
        # Strip markdown code blocks if present
        cleaned = re.sub(r'^```(?:json)?\s*', '', text.strip())
        cleaned = re.sub(r'\s*```$', '', cleaned)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            logger.warning("Failed to parse LLM JSON response, returning raw text")
            return {"titulo": "Análisis Generado", "resumen_general": text, "hallazgos_clave": [], "oportunidades_cross_selling": [], "recomendaciones_estrategicas": [], "tendencias_detectadas": []}
