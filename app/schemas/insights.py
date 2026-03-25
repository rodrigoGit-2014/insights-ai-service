from datetime import date, datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class InsightRequest(BaseModel):
    start_date: date
    end_date: date
    department_id: Optional[str] = None
    section_id: Optional[str] = None
    insight_type: str = Field(default="executive_summary", pattern="^(executive_summary|cross_selling|merchandising|seasonal)$")

class InsightFinding(BaseModel):
    titulo: str
    descripcion: str
    impacto: str
    productos_involucrados: list[str] = []
    metricas: dict = {}

class CrossSellingOpportunity(BaseModel):
    combinacion: list[str]
    confidence: float
    lift: float
    recomendacion_accion: str

class StrategicRecommendation(BaseModel):
    titulo: str
    descripcion: str
    prioridad: str
    tipo: str

class InsightData(BaseModel):
    titulo: str
    resumen_general: str
    hallazgos_clave: list[InsightFinding] = []
    oportunidades_cross_selling: list[CrossSellingOpportunity] = []
    recomendaciones_estrategicas: list[StrategicRecommendation] = []
    tendencias_detectadas: list[str] = []

class TokenUsage(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0

class InsightResponse(BaseModel):
    insight_id: UUID
    insight_type: str
    generated_at: datetime
    data: InsightData
    run_metadata: dict = {}
    token_usage: TokenUsage
    cached: bool = False
