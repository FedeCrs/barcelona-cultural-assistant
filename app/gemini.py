import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

chat_model_name = "gemini-1.5-flash"
chat_model = genai.GenerativeModel(chat_model_name)

def ask_gemini(pregunta: str, contexto: str) -> str:
    try:
        # Detectar si la pregunta explícitamente pide el barrio o la zona
        pregunta_baja = pregunta.lower()
        pide_barrio = "barrio" in pregunta_baja or "vecindario" in pregunta_baja or "zona" in pregunta_baja

        # Ajuste: si no hay contexto de la BD, indicamos que Gemini puede usar conocimiento general
        if contexto.strip() == "":
            contexto_texto = (
                "No se encontró información específica en la base de datos local. "
                "Usa tu conocimiento general sobre Barcelona para responder, "
                "incluyendo nombres y direcciones de locales conocidos como Apolo, Razzmatazz, Paralel 62, etc."
            )
        else:
            contexto_texto = f"Aquí tienes información relevante de la base de datos local:\n{contexto}"

        prompt = f"""
Eres un asistente cultural de Barcelona. Tu objetivo es proporcionar información precisa sobre espacios culturales.
{contexto_texto}

**Instrucciones clave:**
1.  Si la información de la "base de datos local" es directamente relevante y suficiente para responder a la pregunta del usuario, utilízala.
2.  Si la pregunta del usuario es sobre un espacio cultural ya mencionado o encontrado en la base de datos local:
    * Si pregunta explícitamente por el barrio o la zona, solo menciona si estás seguro.
3.  Siempre mantén un tono amable y servicial.



Pregunta del usuario:
{pregunta}
"""
        response = chat_model.generate_content(prompt)
        return response.text.strip()
    
    except Exception as e:
        print(f"Error al procesar la pregunta en ask_gemini: {e}")
        return "Lo siento, hubo un error al procesar tu pregunta en este momento."
