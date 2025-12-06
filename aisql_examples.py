"""
Ejemplos de uso de funciones Snowflake Cortex AISQL con Snowpark y la tabla CODIGO_FACILITO.PUBLIC.EMAILS.

Funciones disponibles:
- AI_COMPLETE: Genera completaciones de texto usando LLMs
- AI_CLASSIFY: Clasifica texto en categorías definidas
- AI_EXTRACT: Extrae información de textos
- AI_SENTIMENT: Analiza sentimiento de texto
- AI_FILTER: Filtra filas basándose en condiciones en lenguaje natural
- AI_TRANSLATE: Traduce texto entre idiomas
- AI_AGG: Analiza y resume múltiples registros de forma agregada
"""
from snowflake.snowpark.exceptions import SnowparkSQLException
from upload_emails_to_snowflake import connection_parameters, Session


def demo_ai_complete(session):
    """Summarize ticket content using AI_COMPLETE."""
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


def demo_ai_classify(session):
    """Classify problem types in tickets using AI_CLASSIFY."""
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


def demo_ai_extract(session):
    """Extract specific information from emails using AI_EXTRACT."""
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


def demo_ai_sentiment(session):
    """Analyze sentiment and tone of tickets using AI_SENTIMENT."""
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


def demo_ai_filter(session):
    """Filter technical problems using AI_FILTER."""
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


def demo_ai_translate(session):
    """Translate ticket descriptions using AI_TRANSLATE."""
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


def demo_ai_agg(session):
    """Get aggregated insights using AI_AGG."""
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


def main():
    """Run all AISQL examples."""
    session = Session.builder.configs(connection_parameters).create()
    
    try:
        demo_ai_complete(session)
        demo_ai_classify(session)
        demo_ai_extract(session)
        demo_ai_sentiment(session)
        demo_ai_filter(session)
        demo_ai_translate(session)
        demo_ai_agg(session)
    finally:
        session.close()


if __name__ == "__main__":
    main()
