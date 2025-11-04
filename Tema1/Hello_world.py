from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0.7)

pregunta = "En cuanto tiempo ganaria buen dinero en mi empresa de agentes con langchain"
print("pregunta: ",pregunta)

respuesta = llm.invoke(pregunta)
print("Respuesta del modelo: ",respuesta.content)