from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import vllm
from typing import Optional, List

app = FastAPI(title="vLLM API", description="API para inferencia de modelos de lenguaje usando vLLM")

# Inicializar el modelo
model = vllm.LLM(model="meta-llama/Meta-Llama-3-8B-Instruct")

class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 100
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.9
    stop: Optional[List[str]] = None

class GenerateResponse(BaseModel):
    text: str
    tokens: int

@app.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    try:
        # Configurar los parámetros de generación
        generation_config = {
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "top_p": request.top_p,
            "stop": request.stop
        }
        
        # Generar texto
        response = model.generate(request.prompt, **generation_config)
        
        return GenerateResponse(
            text=response[0].outputs[0].text,
            tokens=len(response[0].outputs[0].token_ids)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": "meta-llama/Meta-Llama-3-8B-Instruct"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 