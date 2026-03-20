import re
from sqlalchemy.orm import Session
from app import crud, schemas
from app.gemini import ask_gemini
from app.embeddings import get_chroma_collection, generar_embedding  # Si usas embeddings


def limpiar_pregunta(pregunta: str) -> str:
    """
    Elimina palabras comunes y palabras irrelevantes como 'bar', 'pub', etc.
    """
    pregunta = pregunta.lower()
    pregunta = re.sub(r'[^a-záéíóúüñ0-9\s]', '', pregunta)

    palabras_comunes = [
        'donde','queda','esta','es','el','la','los','las','barcelona','en',
        'un','una','hay','por','del','de','al','me','gustaria','saber',
        'necesito','que','su','cuanto','cuesta','se','encuentra',
        'hola','quiero','quieres','me','podrias','informame',
        # Palabras que no aportan al nombre real
        'bar','pub','club','cafe','restaurante','local'
    ]
    palabras = [p for p in pregunta.split() if p not in palabras_comunes and len(p) > 1]
    return " ".join(palabras).strip()


def procesar_pregunta(pregunta: str, db: Session):
    print("🔎 Pregunta recibida:", pregunta)
    
    # 🔹 Detectar cierre del chat
    frases_cierre = ["no", "no gracias", "gracias", "eso es todo", "chau", "adiós", "me voy"]
    if any(frase in pregunta.lower() for frase in frases_cierre):
        return "¡Perfecto! 😊 Me alegra haberte ayudado. ¡Hasta luego! 👋"

    texto_limpio = limpiar_pregunta(pregunta)
    print("Pregunta limpia:", texto_limpio)

    # 1 Buscar en la BD por nombre o dirección
    try:
        resultados_sql = crud.search_espacios_por_nombre_o_direccion(db, texto_limpio)
    except Exception as e:
        print(f"🚨 ERROR en búsqueda SQL: {e}")
        resultados_sql = []

    if resultados_sql:
        r = resultados_sql[0]
        direccion = r.direccion

        if direccion:
            # Pedimos el barrio a Gemini
            direccion_completa = f"{direccion}, Barcelona"
            prompt_barrio = (
                f"La siguiente dirección está en Barcelona: '{direccion_completa}'. "
                "Dime en qué barrio de Barcelona se encuentra. "
                "Responde solo con el nombre del barrio, nada más."
            )
            try:
                barrio = ask_gemini(prompt_barrio, "").strip()
                if not barrio or len(barrio) < 3:
                    barrio = "algún barrio de Barcelona que no logré identificar 🤔"
            except Exception as e:
                print(f"❌ ERROR al pedir barrio a Gemini: {e}")
                barrio = "desconocido 🤔"

            # Construimos la respuesta
            respuesta = (
                f"😉 Claro, el {r.user_name} está en {direccion}, "
                f"en el barrio de {barrio}."
            )
            # Frase de seguimiento
            respuesta += " ¿Necesitas que te ayude con algo más? 🤔"

            return respuesta
        else:
            return f"Tengo registrado **{r.user_name}**, pero aún no tengo su dirección guardada 🤔"

    # 2 Si no está en la BD, buscar en la web con Gemini
    try:
        prompt_busqueda = (
            f"Necesito la dirección exacta en Barcelona de '{texto_limpio}'. "
            "Responde solo con la dirección y nada más."
        )
        direccion = ask_gemini(prompt_busqueda, "").strip()
        print(f"🌍 Dirección obtenida de Gemini: {direccion}")

        if direccion and "Barcelona" in direccion:
            # Pedir barrio a Gemini
            prompt_barrio = (
                f"Dada la dirección: '{direccion}', en Barcelona, "
                "responde únicamente con el nombre del barrio al que pertenece."
            )
            try:
                barrio = ask_gemini(prompt_barrio, "").strip()
                if not barrio or len(barrio) < 3:
                    barrio = "algún barrio de Barcelona que no logré identificar 🤔"
            except Exception as e:
                print(f"❌ ERROR al pedir barrio a Gemini: {e}")
                barrio = "desconocido 🤔"

            # Guardar en la BD
            nuevo_usuario = schemas.UsuarioCreate(
                user_name=texto_limpio.title(),
                direccion=direccion,
                email=None,
                telefono=None
            )
            crud.create_usuario(db, nuevo_usuario)
            print(f"💾 Dirección guardada en la BD: {direccion}")

            return (
                f"📌 He buscado y encontré que **{texto_limpio.title()}** está en **{direccion}**, "
                f"en el barrio de **{barrio}**. Ya lo guardé en mi base de datos para la próxima 😉"
            )
        else:
            return f"😅 No pude encontrar la dirección de **{texto_limpio.title()}** en Barcelona."

    except Exception as e:
        print(f"❌ ERROR al buscar en la web con Gemini: {e}")
        return "Lo siento, no pude encontrar esa dirección en este momento."
