# MindWell Policy Advisor
Agentic AI exam prototype: SvelteKit UI + FastAPI + LangChain `create_agent` + Groq + local MCP evidence server + reusable policy-analysis skill.

## Run backend (Windows)
In `backend`:
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```
Edit `.env` and add your Groq key. Never commit/share it.
```powershell
python -m uvicorn app.main:app --reload --port 8000
```

## Run frontend
In a second terminal, in `frontend`:
```powershell
npm install
npm run dev
```
Open the URL printed by SvelteKit, usually http://localhost:5173.

## Demo prompts
- Should colleges in India introduce optional mindfulness sessions for students?
- How can employers reduce stress while improving access to counselling?
- Compare school-based wellbeing education with expanding access to qualified counsellors.

## Explain honestly
The MCP server searches a small curated catalogue, not the live web. The LLM may make mistakes. Verify source claims. Recommendations are for policy scoping, not clinical advice.
