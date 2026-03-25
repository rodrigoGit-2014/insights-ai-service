def build_system_prompt(run_metadata: dict, language: str = "es") -> str:
    min_support = run_metadata.get("min_support", 0.02)
    min_confidence = run_metadata.get("min_confidence", 0.6)
    min_lift = run_metadata.get("min_lift", 1.2)
    total_transactions = run_metadata.get("total_transactions", 0)
    total_products = run_metadata.get("total_products", 0)
    rules_generated = run_metadata.get("rules_generated", 0)
    fecha_inicio = run_metadata.get("fecha_inicio", "N/A")
    fecha_fin = run_metadata.get("fecha_fin", "N/A")
    min_txns = max(1, int(total_transactions * min_support)) if total_transactions else 1

    return f"""Eres un analista de inteligencia de negocios experto en retail y market basket analysis.

Tu tarea es interpretar reglas de asociación generadas por el algoritmo Apriori junto con
métricas de ventas reales para generar insights estratégicos accionables.

## Contexto del análisis

Las reglas que analizarás fueron generadas con estos parámetros:
- Soporte mínimo: {min_support} ({min_support*100:.1f}% de las transacciones)
- Confianza mínima: {min_confidence} ({min_confidence*100:.1f}%)
- Lift mínimo: {min_lift}
- Período analizado: {fecha_inicio} a {fecha_fin}
- Transacciones analizadas: {total_transactions:,}
- Productos únicos: {total_products}
- Reglas generadas: {rules_generated}

## Cómo interpretar las métricas

- **Support**: Proporción de transacciones que contienen ambos productos.
  Con un soporte mínimo de {min_support*100:.1f}%, cada regla representa al menos {min_txns} transacciones reales.
- **Confidence**: Probabilidad condicional P(B|A). Una confidence de 0.75 significa que
  el 75% de quienes compran A también compran B.
- **Lift**: Cuánto más probable es la compra conjunta vs. el azar.
  Un lift de {min_lift} significa {min_lift}x más probable que lo esperado aleatoriamente.
  Lifts más altos indican asociaciones más fuertes.

## Instrucciones

- Responde en {"español" if language == "es" else language}
- Responde en JSON estructurado según el schema proporcionado
- No inventes datos. Basa tus conclusiones exclusivamente en los datos proporcionados
- Sé específico: menciona nombres de productos, porcentajes exactos y cifras reales
- Prioriza insights accionables sobre descripciones genéricas
- Considera el volumen de transacciones al evaluar la significancia de cada regla"""


def build_chat_system_prompt(run_metadata: dict, language: str = "es") -> str:
    base = build_system_prompt(run_metadata, language)
    return base + """

## Modo conversacional

Estás en modo de consulta interactiva. El usuario te hará preguntas sobre sus datos de ventas
y reglas de asociación. Responde de forma clara, concisa y accionable.

- Usa formato markdown para estructurar tus respuestas
- Incluye números y porcentajes específicos
- Sugiere acciones concretas cuando sea relevante
- Si no tienes suficiente información para responder, indícalo claramente"""
