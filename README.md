# TranscribeYT MVP 🚀

Este é o **TranscribeYT**, um MVP para transcrição de vídeos do YouTube com análise inteligente via IA (GPT-4.1 Mini).

## 🌍 Como Colocar Online (MVP)

### 1. Backend (FastAPI) no Render
Hospede o processamento (Python) em um serviço como o [Render](https://render.com).

- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Variáveis de Ambiente**:
  - `OPENAI_API_KEY`: Sua chave da OpenAI.

### 2. Frontend no Cloudflare Pages
Hospede o site estático no Cloudflare.

- **Build Command**: (Nenhum)
- **Output Directory**: `./`
- **Arquivo principal**: `index.html`

### 3. Conectando Tudo
1. Após o deploy do Backend no Render, você receberá uma URL (ex: `https://meu-backend.onrender.com`).
2. Abra o seu site no Cloudflare Pages.
3. Use a interface de configuração no topo do site para colar a URL do seu backend.
4. Salve e comece a usar!

## 🛠️ Tecnologias
- **Frontend**: HTML5, Vanilla JS, Tailwind CSS, Marked.js.
- **Backend**: Python, FastAPI, OpenAI API, YouTube Transcript API.

---
*MVP desenvolvido com auxílio de Antigravity AI.*

