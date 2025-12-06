"""
Ejemplos de uso de funciones Snowflake Cortex AISQL con Snowpark y la tabla CODIGO_FACILITO.PUBLIC.EMAILS.

Funciones disponibles:
- AI_COMPLETE: Genera completaciones de texto usando LLMs
- AI_CLASSIFY: Clasifica texto en categorías definidas
- AI_EXTRACT: Extrae información de textos
- AI_SENTIMENT: Analiza sentimiento de texto
- AI_FILTER: Filtra filas basándose en condiciones en lenguaje natural
- AI_TRANSLATE: Traduce texto entre idiomas
"""
from snowflake.snowpark.exceptions import SnowparkSQLException
from upload_emails_to_snowflake import connection_parameters, Session

# Crear una nueva sesión para este script
session = Session.builder.configs(connection_parameters).create()

# 1. AI_COMPLETE: Generar completaciones de texto
# Ejemplo: Resumir el contenido del ticket en una línea
print("\n=== 1. AI_COMPLETE: Resumir contenido del ticket ===")
try:
    result = session.sql("""
        SELECT 
            TICKET_ID,
            CONTENT,
            AI_COMPLETE(
                'mistral-large2',
                CONCAT('Resume en una línea el siguiente ticket de soporte: ', CONTENT)
            ) AS CONTENT_SUMMARY
        FROM CODIGO_FACILITO.PUBLIC.EMAILS
        LIMIT 5
    """).collect()
    for row in result:
        print(f"Ticket {row['TICKET_ID']}: {row['CONTENT_SUMMARY']}")
except SnowparkSQLException as e:
    print(f"Error en AI_COMPLETE: {e}")

# 2. AI_CLASSIFY: Clasificar tipo de problema en el ticket
# Ejemplo: Clasificar los tickets por categoría de problema
print("\n=== 2. AI_CLASSIFY: Clasificar tipo de problema ===")
try:
    result = session.sql("""
        SELECT 
            TICKET_ID,
            CONTENT,
            AI_CLASSIFY(
                CONTENT,
                ['Reembolso', 'Problema técnico', 'Transferencia de ticket', 'Feedback', 'Otro']
            ):labels[0] AS PROBLEM_CATEGORY
        FROM CODIGO_FACILITO.PUBLIC.EMAILS
        LIMIT 5
    """).collect()
    for row in result:
        print(f"Ticket {row['TICKET_ID']}: Categoría: {row['PROBLEM_CATEGORY']}")
except SnowparkSQLException as e:
    print(f"Error en AI_CLASSIFY: {e}")

# 3. AI_EXTRACT: Extraer información específica del email
# Ejemplo: Extraer el número de orden (Order #) del ticket
print("\n=== 3. AI_EXTRACT: Extraer número de orden del ticket ===")
try:
    result = session.sql("""
        SELECT 
            TICKET_ID,
            CONTENT,
            AI_EXTRACT(
                CONTENT,
                'Extrae el número de orden (Order #) si existe en el contenido'
            ) AS ORDER_NUMBER
        FROM CODIGO_FACILITO.PUBLIC.EMAILS
        LIMIT 5
    """).collect()
    for row in result:
        print(f"Ticket {row['TICKET_ID']}: Orden: {row['ORDER_NUMBER']}")
except SnowparkSQLException as e:
    print(f"Error en AI_EXTRACT: {e}")

# 4. AI_SENTIMENT: Analizar si el email se ve "profesional" o "informal"
# (Aunque emails son típicamente simples, esto es un ejemplo de uso)
print("\n=== 4. AI_SENTIMENT: Analizar tono del ticket ===")
try:
    result = session.sql("""
        SELECT 
            TICKET_ID,
            CONTENT,
            AI_SENTIMENT(
                CONTENT
            ) AS SENTIMENT_SCORE
        FROM CODIGO_FACILITO.PUBLIC.EMAILS
        LIMIT 5
    """).collect()
    for row in result:
        print(f"Ticket {row['TICKET_ID']}: Sentimiento: {row['SENTIMENT_SCORE']}")
except SnowparkSQLException as e:
    print(f"Error en AI_SENTIMENT: {e}")

# 5. AI_FILTER: Filtrar emails que contienen "gmail"
# Ejemplo: Mantener solo emails de Gmail usando AI_FILTER
print("\n=== 5. AI_FILTER: Filtrar tickets con problemas técnicos ===")
try:
    result = session.sql("""
        SELECT 
            TICKET_ID,
            CONTENT
        FROM CODIGO_FACILITO.PUBLIC.EMAILS
        WHERE AI_FILTER(CONCAT('¿Este ticket contiene un problema técnico o error de la app?', CONTENT)) = TRUE
        LIMIT 5
    """).collect()
    print(f"Encontrados {len(result)} tickets con problemas técnicos:")
    for row in result:
        print(f"  - Ticket {row['TICKET_ID']}: {row['CONTENT'][:100]}...")
except SnowparkSQLException as e:
    print(f"Error en AI_FILTER: {e}")

# 6. AI_TRANSLATE: Traducir texto relacionado con email
# Ejemplo: Describir el email en español
print("\n=== 6. AI_TRANSLATE: Traducir descripción de ticket ===")
try:
    result = session.sql("""
        SELECT 
            TICKET_ID,
            CONTENT,
            AI_TRANSLATE(
                AI_COMPLETE(
                    'mistral-7b',
                    CONCAT('Describe brevemente en inglés este ticket de soporte: ', CONTENT)
                ),
                'en',
                'es'
            ) AS DESCRIPCION_ES
        FROM CODIGO_FACILITO.PUBLIC.EMAILS
        LIMIT 3
    """).collect()
    for row in result:
        print(f"Ticket {row['TICKET_ID']}:")
        print(f"  Contenido: {row['CONTENT'][:80]}...")
        print(f"  Descripción: {row['DESCRIPCION_ES']}\n")
except SnowparkSQLException as e:
    print(f"Error en AI_TRANSLATE: {e}")

# 7. Análisis agregado: Resumen de emails con AI_AGG
# Ejemplo: Obtener insights sobre todos los dominios de email
print("\n=== 7. AI_AGG: Resumen de dominios de email ===")
try:
    result = session.sql("""
        SELECT 
            AI_AGG(
                CONTENT,
                'Lista los 3 temas principales mencionados en los tickets de soporte. Sé conciso.'
            ) AS CONTENT_SUMMARY
        FROM CODIGO_FACILITO.PUBLIC.EMAILS
    """).collect()
    for row in result:
        print(f"Resumen: {row['CONTENT_SUMMARY']}")
except SnowparkSQLException as e:
    print(f"Error en AI_AGG: {e}")

session.close()
