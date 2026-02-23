import os
import hashlib
from openai import OpenAI

# Initialize client (expects OPENAI_API_KEY in environment)
client = OpenAI()

# Model and configuration
MODEL = "gpt-4.1-mini"
TEMPERATURE = 0.3

# System instruction to keep responses direct
SYSTEM_INSTRUCTION = (
    "Você é um assistente analítico. RESPONDA DIRETAMENTE ao que foi pedido. "
    "NÃO use introduções como 'Claro!', 'Aqui está' ou 'Certo'. "
    "NÃO use conclusões ou ofereça ajuda adicional ao final. "
    "Responda apenas com o conteúdo solicitado."
)

# Analysis prompts
PROMPTS = {
    "summary": "Crie um resumo inteligente, claro e conciso deste conteúdo: {text}",
    "bullets": "Extraia pontos-chave em bullet points para um aprendizado rápido e eficiente: {text}",
    "checklist": "Transforme este conteúdo em um checklist prático de ações a serem seguidas: {text}",
    "insights": "Extraia insights avançados, implicações e observações críticas deste texto: {text}",
    "simplify": "Explique este conteúdo de forma extremamente simples, como para uma criança ou iniciante: {text}",
    "detailed": "Forneça uma explicação detalhada e profunda deste conteúdo, explorando nuances e sub-tópicos: {text}",
    "chapters": "Divida este conteúdo em capítulos automáticos com títulos e descrições breves: {text}",
    "concepts": "Extraia e explique brevemente os conceitos fundamentais abordados: {text}",
    "study_plan": "Crie um plano de estudo estruturado e passo-a-passo baseado neste conteúdo: {text}",
    "translate": "Traduza o conteúdo abaixo para o Português do Brasil, mantendo a fidelidade e o tom: {text}",
    "mindmap": "Crie uma estrutura de Mapa Mental organizada por tópicos principais e ramificações: {text}",
    "qa": "Crie perguntas e respostas baseadas neste conteúdo: {text}"
}

# Simple in-memory cache
_cache = {}

def analyze_text(mode: str, text: str) -> str:
    """
    Processes text with OpenAI based on the selected mode.
    Uses a simple in-memory cache to avoid duplicate calls.
    """
    if mode not in PROMPTS:
        raise ValueError(f"Modo de análise inválido: {mode}")

    if not text.strip():
        raise ValueError("O texto para análise não pode estar vazio.")

    # Create cache key
    cache_key = f"{mode}:{hash(text)}"

    if cache_key in _cache:
        return _cache[cache_key]

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": PROMPTS[mode].format(text=text)}
            ],
            temperature=TEMPERATURE
        )

        result = response.choices[0].message.content.strip()
        _cache[cache_key] = result
        return result

    except Exception as e:
        # Robust error handling for OpenAI calls
        raise RuntimeError(f"Erro ao processar com OpenAI: {str(e)}")
