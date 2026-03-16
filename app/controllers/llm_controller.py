from app.services.llm_service import chat

def chatGPT(msg:str):
    return chat(msg)

def startChat(msg:str):
    return chat(msg)