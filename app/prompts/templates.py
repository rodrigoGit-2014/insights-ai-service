INSIGHT_TEMPLATES = {
    "executive_summary": """Analiza los siguientes datos de ventas y reglas de asociación para generar un resumen ejecutivo.

DATOS DE VENTAS:
{sales_context}

REGLAS DE ASOCIACIÓN (las más relevantes):
{rules_context}

RESUMEN DE TRANSACCIONES:
{transaction_summary}

Genera un JSON con esta estructura exacta:
{{
  "titulo": "Resumen Ejecutivo de Inteligencia Comercial",
  "resumen_general": "2-3 párrafos de resumen ejecutivo del comportamiento de compra",
  "hallazgos_clave": [
    {{
      "titulo": "string con el hallazgo",
      "descripcion": "explicación detallada del hallazgo",
      "impacto": "alto|medio|bajo",
      "productos_involucrados": ["producto1", "producto2"],
      "metricas": {{"confidence": 0.75, "lift": 2.3}}
    }}
  ],
  "oportunidades_cross_selling": [
    {{
      "combinacion": ["producto_a", "producto_b"],
      "confidence": 0.72,
      "lift": 2.1,
      "recomendacion_accion": "acción específica para aprovechar esta asociación"
    }}
  ],
  "recomendaciones_estrategicas": [
    {{
      "titulo": "nombre de la recomendación",
      "descripcion": "detalle de qué hacer y por qué",
      "prioridad": "alta|media|baja",
      "tipo": "merchandising|pricing|promocion|inventario"
    }}
  ],
  "tendencias_detectadas": ["tendencia 1", "tendencia 2"]
}}

Responde SOLO con el JSON, sin texto adicional.""",

    "cross_selling": """Analiza las reglas de asociación para identificar oportunidades de venta cruzada y bundles.

DATOS DE VENTAS:
{sales_context}

REGLAS DE ASOCIACIÓN:
{rules_context}

Genera un JSON con esta estructura:
{{
  "titulo": "Oportunidades de Cross-Selling",
  "resumen_general": "resumen de las principales oportunidades de venta cruzada detectadas",
  "hallazgos_clave": [
    {{
      "titulo": "nombre del hallazgo",
      "descripcion": "detalle",
      "impacto": "alto|medio|bajo",
      "productos_involucrados": ["p1", "p2"],
      "metricas": {{}}
    }}
  ],
  "oportunidades_cross_selling": [
    {{
      "combinacion": ["producto_a", "producto_b"],
      "confidence": 0.72,
      "lift": 2.1,
      "recomendacion_accion": "bundle sugerido, descuento combo, colocación en góndola, etc."
    }}
  ],
  "recomendaciones_estrategicas": [
    {{
      "titulo": "recomendación",
      "descripcion": "detalle",
      "prioridad": "alta|media|baja",
      "tipo": "merchandising|pricing|promocion|inventario"
    }}
  ],
  "tendencias_detectadas": []
}}

Responde SOLO con el JSON.""",

    "merchandising": """Analiza las reglas de asociación para generar recomendaciones de merchandising y layout de tienda.

DATOS DE VENTAS:
{sales_context}

REGLAS DE ASOCIACIÓN:
{rules_context}

RESUMEN DE TRANSACCIONES:
{transaction_summary}

Genera un JSON con esta estructura exacta:
{{
  "titulo": "Análisis de Merchandising y Layout",
  "resumen_general": "2-3 párrafos sobre oportunidades de merchandising basadas en los patrones de compra",
  "hallazgos_clave": [
    {{
      "titulo": "string con el hallazgo",
      "descripcion": "explicación detallada enfocada en colocación de productos y layout",
      "impacto": "alto|medio|bajo",
      "productos_involucrados": ["producto1", "producto2"],
      "metricas": {{"confidence": 0.75, "lift": 2.3}}
    }}
  ],
  "oportunidades_cross_selling": [
    {{
      "combinacion": ["producto_a", "producto_b"],
      "confidence": 0.72,
      "lift": 2.1,
      "recomendacion_accion": "colocación en góndola, zona caliente, cabecera, etc."
    }}
  ],
  "recomendaciones_estrategicas": [
    {{
      "titulo": "nombre de la recomendación de merchandising",
      "descripcion": "detalle de qué hacer con el layout y por qué",
      "prioridad": "alta|media|baja",
      "tipo": "merchandising|pricing|promocion|inventario"
    }}
  ],
  "tendencias_detectadas": ["tendencia 1", "tendencia 2"]
}}

Enfócate en colocación de productos, layout de góndola, y zonas calientes.
Responde SOLO con el JSON, sin texto adicional.""",

    "seasonal": """Analiza las tendencias de ventas mensuales y reglas de asociación para detectar patrones estacionales.

TENDENCIAS MENSUALES:
{monthly_trend}

REGLAS DE ASOCIACIÓN:
{rules_context}

DATOS DE VENTAS:
{sales_context}

RESUMEN DE TRANSACCIONES:
{transaction_summary}

Genera un JSON con esta estructura exacta:
{{
  "titulo": "Análisis de Estacionalidad y Patrones Temporales",
  "resumen_general": "2-3 párrafos sobre patrones estacionales detectados en los datos de ventas",
  "hallazgos_clave": [
    {{
      "titulo": "string con el hallazgo estacional",
      "descripcion": "explicación detallada del patrón temporal detectado",
      "impacto": "alto|medio|bajo",
      "productos_involucrados": ["producto1", "producto2"],
      "metricas": {{"confidence": 0.75, "lift": 2.3}}
    }}
  ],
  "oportunidades_cross_selling": [
    {{
      "combinacion": ["producto_a", "producto_b"],
      "confidence": 0.72,
      "lift": 2.1,
      "recomendacion_accion": "acción estacional específica para aprovechar esta asociación"
    }}
  ],
  "recomendaciones_estrategicas": [
    {{
      "titulo": "nombre de la recomendación estacional",
      "descripcion": "detalle de planificación temporal y estacional",
      "prioridad": "alta|media|baja",
      "tipo": "merchandising|pricing|promocion|inventario"
    }}
  ],
  "tendencias_detectadas": ["tendencia estacional 1", "tendencia estacional 2"]
}}

Enfócate en estacionalidad, picos de demanda, y planificación temporal.
Responde SOLO con el JSON, sin texto adicional.""",
}
