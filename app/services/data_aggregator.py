import logging
import asyncio
from typing import Optional
import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)

class DataAggregator:
    def __init__(self, auth_token: str):
        self.sales_url = settings.SALES_SERVICE_URL
        self.apriori_url = settings.APRIORI_SERVICE_URL
        self.headers = {"Authorization": f"Bearer {auth_token}"}

    async def gather_context(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        department_id: Optional[str] = None,
        section_id: Optional[str] = None,
    ) -> dict:
        params = {}
        if start_date:
            params["fecha_inicio"] = start_date
        if end_date:
            params["fecha_fin"] = end_date

        apriori_params = {}
        if start_date:
            apriori_params["start_date"] = start_date
        if end_date:
            apriori_params["end_date"] = end_date
        if department_id:
            apriori_params["department_id"] = department_id
        if section_id:
            apriori_params["section_id"] = section_id

        async with httpx.AsyncClient(timeout=30, headers=self.headers) as client:
            tasks = [
                client.get(f"{self.sales_url}/sales/total", params=params),
                client.get(f"{self.sales_url}/sales/monthly-trend", params=params),
                client.get(f"{self.sales_url}/analytics/departments", params=params),
                client.get(f"{self.sales_url}/analytics/products/top-revenue", params={**params, "limit": 20}),
                client.get(f"{self.sales_url}/analytics/customers/average-spend", params=params),
                client.get(f"{self.apriori_url}/transactions/summary", params=apriori_params),
                client.get(f"{self.apriori_url}/analysis/runs", params={"limit": 1}),
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)

        context = {
            "sales_total": self._safe_json(results[0]),
            "monthly_trend": self._safe_json(results[1]),
            "departments": self._safe_json(results[2]),
            "top_products": self._safe_json(results[3]),
            "customer_spend": self._safe_json(results[4]),
            "transaction_summary": self._safe_json(results[5]),
            "latest_run": None,
            "rules": [],
            "run_metadata": {},
        }

        # Get latest run metadata and rules
        runs_data = self._safe_json(results[6])
        if runs_data and runs_data.get("runs"):
            latest_run = runs_data["runs"][0]
            context["latest_run"] = latest_run
            context["run_metadata"] = latest_run

            # Fetch rules for this run
            try:
                async with httpx.AsyncClient(timeout=30, headers=self.headers) as client:
                    run_detail = await client.get(
                        f"{self.apriori_url}/analysis/runs/{latest_run['id']}"
                    )
                    if run_detail.status_code == 200:
                        detail = run_detail.json()
                        context["rules"] = detail.get("rules", [])
            except Exception as e:
                logger.warning(f"Failed to fetch run rules: {e}")

        return context

    def _safe_json(self, response) -> Optional[dict]:
        if isinstance(response, Exception):
            logger.warning(f"Request failed: {response}")
            return None
        try:
            if response.status_code == 200:
                return response.json()
            logger.warning(f"Non-200 response: {response.status_code}")
            return None
        except Exception:
            return None

    @staticmethod
    def select_priority_rules(rules: list, top_products: list = None, max_rules: int = 30) -> list:
        if not rules:
            return []
        top_products = top_products or []
        top_product_names = [p.get("nombre_producto", p.get("product", "")) for p in top_products[:10]]

        by_lift = sorted(rules, key=lambda r: r.get("lift", 0), reverse=True)[:10]
        by_conf = sorted(rules, key=lambda r: r.get("confidence", 0), reverse=True)[:10]
        by_supp = sorted(rules, key=lambda r: r.get("support", 0), reverse=True)[:5]

        product_relevant = []
        for r in rules:
            products_in_rule = r.get("antecedent", []) + r.get("consequent", [])
            if any(p in products_in_rule for p in top_product_names):
                product_relevant.append(r)
                if len(product_relevant) >= 5:
                    break

        # Deduplicate
        seen = set()
        selected = []
        for r in by_lift + by_conf + by_supp + product_relevant:
            key = (tuple(sorted(r.get("antecedent", []))), tuple(sorted(r.get("consequent", []))))
            if key not in seen:
                seen.add(key)
                selected.append(r)
                if len(selected) >= max_rules:
                    break

        return selected
