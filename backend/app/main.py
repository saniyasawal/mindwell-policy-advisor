import os, sys
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient

BASE = Path(__file__).resolve().parents[1]
load_dotenv(BASE / ".env")
SKILL = BASE / "skills" / "policy_analysis.md"

class Request(BaseModel):
    question: str = Field(min_length=8, max_length=1200)
    population: str = "Students and young adults"
    context: str = "India"

app = FastAPI(title="MindWell Policy Advisor API")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173","http://127.0.0.1:5173"], allow_methods=["*"], allow_headers=["*"])

@app.get("/api/health")
def health():
    return {"status":"ok","llm_configured":bool(os.getenv("GROQ_API_KEY")),"framework":"LangChain create_agent","mcp":"FastMCP stdio"}

@app.post("/api/policy")
async def policy(req: Request):
    if not os.getenv("GROQ_API_KEY"):
        raise HTTPException(503, "GROQ_API_KEY missing. Add it to backend/.env and restart.")
    try:
        skill = SKILL.read_text(encoding="utf-8")
        client = MultiServerMCPClient({"evidence":{"transport":"stdio","command":sys.executable,"args":[str(BASE / "mcp_server.py")]}})
        tools = await client.get_tools()
        model_name = os.getenv("GROQ_MODEL","llama-3.3-70b-versatile")
        agent = create_agent(
            model=ChatGroq(model=model_name, temperature=0.1),
            tools=tools,
            system_prompt=f"""You are MindWell Policy Advisor, an evidence-aware public policy assistant, not a therapist.
Population: {req.population}. Geographic context: {req.context}.
MUST call search_policy_evidence before evidence-based claims. Cite source titles and URLs from tool results.
Never invent statistics, effect sizes, budgets or citations. Separate sourced facts, policy inference and uncertainty.
Consider feasibility, equity, privacy, cultural acceptability, voluntary participation, workload, opportunity cost, safeguarding and referral access.
Do not claim mindfulness cures mental illness or replaces professional care.
Use these headings: 1 Executive recommendation 2 Options and rationale 3 Evidence and links 4 Implementation plan 5 Benefits and trade-offs 6 Risks, safeguards and equity 7 Evaluation metrics 8 Evidence gaps.
Policy-analysis skill:
{skill}"""
        )
        result = await agent.ainvoke({"messages":[{"role":"user","content":f"Question: {req.question}\nPopulation: {req.population}\nContext: {req.context}\nUse the evidence tool and produce a balanced policy brief."}]})
        messages = result.get("messages", [])
        answer = str(messages[-1].content) if messages else "No answer returned."
        used = any(getattr(m,"type","") == "tool" for m in messages)
        return {"answer":answer,"tool_used":used,"model":model_name,"evidence_sources":[
            "WHO Guidelines on Mental Health at Work — https://www.who.int/publications/i/item/9789240053052",
            "WHO World Mental Health Report — https://www.who.int/publications/i/item/9789240049338",
            "WHO Doing What Matters in Times of Stress — https://www.who.int/publications/i/item/9789240003927",
            "WHO/UNESCO Making Every School a Health-Promoting School — https://www.who.int/publications/i/item/9789240025073",
            "NICE Depression in Adults — https://www.nice.org.uk/guidance/ng222"],
            "limitations":["Curated evidence catalogue; not a live systematic review.","LLM outputs can contain errors; verify sources.","Local costing, consultation and pilot evaluation are needed."]}
    except Exception as e:
        raise HTTPException(500, f"Agent failed: {type(e).__name__}: {e}")
