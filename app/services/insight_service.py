import logging
import json
import uuid
from datetime import datetime, timezone
from typing import Optional
from app.core.cache import cache, make_cache_key
from app.services.data_aggregator import DataAggregator
from app.services.llm_service import LLMService
from app.prompts.system import build_system_prompt
from app.prompts.templates import INSIGHT_TEMPLATES

logger = logging.getLogger(__name__)

class InsightService:
    def __init__(self):
        self.llm = LLMService()

    async def generate_insight(
        self,
        auth_token: str,
        company_id: str,
        insight_type: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        department_id: Optional[str] = None,
        section_id: Optional[str] = None,
    ) -> dict:
        # Check cache
        cache_key = make_cache_key(
            "insight", company_id=str(company_id), insight_type=insight_type,
            start_date=start_date, end_date=end_date,
            department_id=department_id, section_id=section_id,
        )
        cached = cache.get(cache_key)
        if cached:
            cached["cached"] = True
            return cached

        # Aggregate data
        aggregator = DataAggregator(auth_token)
        context = await aggregator.gather_context(start_date, end_date, department_id, section_id)

        # Select priority rules
        top_products = context.get("top_products", {}).get("data", []) if context.get("top_products") else []
        priority_rules = DataAggregator.select_priority_rules(context.get("rules", []), top_products)

        # Build prompts
        run_metadata = context.get("run_metadata", {})
        system_prompt = build_system_prompt(run_metadata)
        template = INSIGHT_TEMPLATES.get(insight_type, INSIGHT_TEMPLATES["executive_summary"])
        user_prompt = template.format(
            sales_context=json.dumps(context.get("sales_total", {}), indent=2, default=str),
            rules_context=json.dumps(priority_rules, indent=2, default=str),
            transaction_summary=json.dumps(context.get("transaction_summary", {}), indent=2, default=str),
            monthly_trend=json.dumps(context.get("monthly_trend", {}), indent=2, default=str),
        )

        # Generate
        data, usage = self.llm.generate(system_prompt, user_prompt)

        result = {
            "insight_id": str(uuid.uuid4()),
            "insight_type": insight_type,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "data": data,
            "run_metadata": run_metadata,
            "token_usage": usage,
            "cached": False,
        }

        # Cache result
        cache.set(cache_key, result)

        return result

    async def generate_insight_stream(
        self,
        auth_token: str,
        company_id: str,
        insight_type: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        department_id: Optional[str] = None,
        section_id: Optional[str] = None,
    ):
        aggregator = DataAggregator(auth_token)
        context = await aggregator.gather_context(start_date, end_date, department_id, section_id)

        top_products = context.get("top_products", {}).get("data", []) if context.get("top_products") else []
        priority_rules = DataAggregator.select_priority_rules(context.get("rules", []), top_products)

        run_metadata = context.get("run_metadata", {})
        system_prompt = build_system_prompt(run_metadata)
        template = INSIGHT_TEMPLATES.get(insight_type, INSIGHT_TEMPLATES["executive_summary"])
        user_prompt = template.format(
            sales_context=json.dumps(context.get("sales_total", {}), indent=2, default=str),
            rules_context=json.dumps(priority_rules, indent=2, default=str),
            transaction_summary=json.dumps(context.get("transaction_summary", {}), indent=2, default=str),
            monthly_trend=json.dumps(context.get("monthly_trend", {}), indent=2, default=str),
        )

        yield json.dumps({"type": "metadata", "run_metadata": run_metadata}) + "\n"

        for chunk in self.llm.generate_stream(system_prompt, user_prompt):
            yield chunk

    async def generate_chat_stream(
        self,
        auth_token: str,
        company_id: str,
        messages: list,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ):
        from app.prompts.system import build_chat_system_prompt
        aggregator = DataAggregator(auth_token)
        context = await aggregator.gather_context(start_date, end_date)

        top_products = context.get("top_products", {}).get("data", []) if context.get("top_products") else []
        priority_rules = DataAggregator.select_priority_rules(context.get("rules", []), top_products)

        run_metadata = context.get("run_metadata", {})
        system_prompt = build_chat_system_prompt(run_metadata)

        # Inject context into first user message
        context_injection = f"""
Datos de ventas disponibles:
{json.dumps(context.get("sales_total", {}), indent=2, default=str)}

Reglas de asociación relevantes:
{json.dumps(priority_rules[:15], indent=2, default=str)}

Resumen de transacciones:
{json.dumps(context.get("transaction_summary", {}), indent=2, default=str)}
"""
        chat_messages = []
        for i, m in enumerate(messages):
            if i == 0 and m["role"] == "user":
                chat_messages.append({"role": "user", "content": context_injection + "\n\nPregunta del usuario: " + m["content"]})
            else:
                chat_messages.append(m)

        for chunk in self.llm.generate_chat(system_prompt, chat_messages):
            yield chunk
