# MindWell Policy Advisor
### An Evidence-Aware AI Agent for Student Mental Wellbeing Policy Analysis

MindWell Policy Advisor is an AI-powered policy decision-support prototype that helps users explore practical policies for student mental wellbeing. It uses a tool-calling AI agent to retrieve information from a curated public-health evidence catalogue and generate structured policy briefs covering recommendations, implementation, feasibility, risks, equity, trade-offs and evaluation.

The project was developed as part of the **Advanced AI Core Lab — Agentic AI track**, with an emphasis on agent frameworks, tool calling, Model Context Protocol (MCP), skills, API integration and a user-friendly interface.

> **Important distinction:** The project draws philosophical inspiration from Swami Bhoomananda Tirtha's article *“Let Mind Think And You Simply Be”*. The article informs the general theme of observing thoughts and approaching mental wellbeing thoughtfully. It is not treated as scientific evidence that a particular mental-health intervention is effective. Policy recommendations are informed by the project's curated public-health sources and should be independently verified.

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Objectives](#objectives)
- [Article Inspiration](#article-inspiration)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Agent Workflow](#agent-workflow)
- [Agentic AI Components](#agentic-ai-components)
- [Evidence Catalogue](#evidence-catalogue)
- [Installation and Setup](#installation-and-setup)
- [Environment Configuration](#environment-configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Example Use Case](#example-use-case)
- [Responsible AI and Safeguards](#responsible-ai-and-safeguards)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Project Structure](#project-structure)
- [Learning Outcomes](#learning-outcomes)
- [Disclaimer](#disclaimer)

## Problem Statement

Student mental wellbeing is influenced by several factors, including academic workload, institutional culture, access to support services, social circumstances and individual stress-management needs.

Institutions considering wellbeing initiatives need to evaluate more than individual coping techniques. They must also consider feasibility, accessibility, privacy, student participation, staff capacity, safeguarding and referral pathways.

Finding and translating relevant public-health guidance into a practical policy brief can be time-consuming, particularly when decision-makers need a structured comparison of options and their potential trade-offs.

MindWell Policy Advisor explores how an agentic AI system can assist with this process by retrieving relevant entries from a curated evidence catalogue and generating a structured, evidence-aware policy brief.

## Objectives

The main objectives are to:

1. Develop an AI agent that supports public-policy analysis for student mental wellbeing.
2. Integrate an LLM with a tool-calling agent framework.
3. Use MCP to expose a Python-based evidence-search tool to the agent.
4. Use a policy-analysis skill to guide the agent's reasoning and report structure.
5. Generate policy briefs containing recommendations, implementation plans, trade-offs, safeguards and evaluation metrics.
6. Build a web interface that allows users to submit policy questions and view generated reports.
7. Identify limitations, uncertainties and responsible-use considerations when applying generative AI to policy decisions.

## Article Inspiration

**Article:** *“Let Mind Think And You Simply Be”*  
**Author:** Swami Bhoomananda Tirtha

The article provides a philosophical starting point for considering how people relate to their thoughts. Its broad themes include observing thoughts, avoiding unnecessary struggle with every thought, allowing some thoughts to pass and cultivating a more balanced approach to the mind.

The project translates this general inspiration into a secular policy question:

*How might educational institutions support student wellbeing while respecting individual choice and recognising the importance of institutional and professional support?*

The system does not promote a religious practice or assume that a philosophical perspective is a clinical intervention. It considers optional stress-management education as one possible component of a wider wellbeing policy, alongside workload review, counselling access and appropriate referral pathways.

## Key Features

- **AI-generated policy briefs:** Produces structured reports in response to user-defined policy questions.
- **Tool-calling agent:** Uses a LangChain agent that can invoke an evidence-search tool.
- **MCP integration:** Connects the agent to a local FastMCP server using standard input/output (stdio).
- **Curated evidence retrieval:** Searches five predefined public-health and clinical-guidance entries.
- **Policy-analysis skill:** Supplies domain-specific instructions for balanced policy analysis.
- **Structured output:** Organises recommendations, implementation plans, benefits, trade-offs, risks and evaluation metrics under defined headings.
- **Source links and caveats:** Provides source references and communicates limitations.
- **Interactive web interface:** Accepts a question, target population and geographic context.
- **Backend API:** Exposes health-check and policy-generation endpoints through FastAPI.
- **Responsible-use boundaries:** Avoids presenting the application as a diagnostic or treatment system.

## Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Programming language | Python | Agent orchestration, API and MCP server |
| LLM provider | Groq | Hosts the language model used for generation |
| Language model | Configured through `GROQ_MODEL` | Generates and structures policy analysis |
| Agent framework | LangChain `create_agent` | Creates a tool-using AI agent |
| API framework | FastAPI | Exposes the backend endpoints |
| Data validation | Pydantic | Validates incoming request fields |
| Tool protocol | Model Context Protocol (MCP) | Connects the agent to the evidence-search tool |
| MCP implementation | FastMCP | Defines and runs the local MCP server |
| MCP client integration | `langchain-mcp-adapters` | Discovers and adapts MCP tools for the agent |
| Frontend | SvelteKit and Svelte | Provides the user interface |
| Report rendering | Marked and DOMPurify | Converts Markdown to HTML and sanitises rendered content |
| Configuration | `python-dotenv` | Loads environment variables from a local `.env` file |
| Evidence storage | Python catalogue | Stores predefined source metadata, summaries and caveats |

The exact model is selected through the `GROQ_MODEL` environment variable. 

## System Architecture

The application uses a frontend–backend architecture with an agent and a local MCP evidence service.

```text
+--------------------------------------+
|       SvelteKit Frontend             |
|                                      |
|  Policy Question                     |
|  Target Population                   |
|  Geographic Context                  |
+------------------+-------------------+
                   |
                   | HTTP POST /api/policy
                   v
+--------------------------------------+
|          FastAPI Backend             |
|                                      |
|  Request Validation (Pydantic)       |
|  Skill Loading                       |
|  Agent Initialization                |
+------------------+-------------------+
                   |
                   v
+--------------------------------------+
|      LangChain create_agent          |
|                                      |
|      Groq-hosted LLM                 |
|      Policy Analysis Instructions    |
+------------------+-------------------+
                   |
                   | MCP tool call
                   v
+--------------------------------------+
|       MCP Client (stdio)             |
+------------------+-------------------+
                   |
                   v
+--------------------------------------+
|       FastMCP Evidence Server        |
|                                      |
|       search_policy_evidence         |
+------------------+-------------------+
                   |
                   v
+--------------------------------------+
|        Curated Evidence Catalogue    |
|                                      |
|  Source titles, topics, summaries,   |
|  URLs and caveats                    |
+--------------------------------------+
```

After receiving evidence results, the agent generates a policy brief. The backend returns the answer and associated metadata to the frontend, where the report is displayed.

## Agent Workflow

The application's workflow is:

1. **Input collection:** The user submits a policy question, target population and geographic context.
2. **Request validation:** FastAPI and Pydantic validate the incoming request.
3. **Skill loading:** The backend loads the policy-analysis instructions from `backend/skills/policy_analysis.md`.
4. **Agent creation:** LangChain `create_agent` is configured with the Groq-hosted LLM, the system prompt and the available MCP tools.
5. **Evidence retrieval:** The agent is instructed to call `search_policy_evidence` before making evidence-based claims.
6. **Catalogue search:** The MCP server ranks catalogue entries using keyword matching and returns up to four matching entries, or three fallback entries if there are no matches.
7. **Policy synthesis:** The LLM uses the available information and policy-analysis instructions to prepare a structured response.
8. **Response delivery:** FastAPI returns the generated report and response metadata.
9. **Report presentation:** The frontend renders the Markdown report for the user.

The tool call is requested through the agent instructions, but the implementation does not independently guarantee that every possible LLM response will follow that instruction.

## Agentic AI Components

### 1. Large Language Model (LLM)

The application uses a Groq-hosted language model through the `ChatGroq` integration.

The LLM is responsible for interpreting the policy question, synthesising the retrieved information, discussing trade-offs and producing the final report.

The model name is configurable using `GROQ_MODEL`. The implementation uses a low temperature setting of `0.1` to encourage more consistent responses.

### 2. Agent Framework — LangChain `create_agent`

LangChain's `create_agent` constructs the tool-using agent.

The agent is configured with:

- The language model.
- A system prompt defining the role and safety boundaries.
- The policy-analysis skill instructions.
- The MCP-discovered evidence-search tool.

The agent can call the tool and use its results as part of generating a response. This is a single-agent design rather than a multi-agent system.

### 3. Tool Calling

**Tool name:** `search_policy_evidence`

The tool accepts a query string and returns a dictionary containing:

- The original query.
- The catalogue size.
- Matching source entries.
- Source titles and URLs.
- Topic descriptions.
- Summaries and caveats.

The tool is implemented in `backend/mcp_server.py` and registered using the `@mcp.tool()` decorator.

### 4. Model Context Protocol (MCP)

MCP provides a standardised way for the AI application to discover and call tools exposed by an MCP server.

In this project:

- FastMCP creates the local evidence server.
- The backend creates an MCP client using `MultiServerMCPClient`.
- The client starts the server as a local subprocess.
- The transport is `stdio`.
- `get_tools()` discovers the available tools and makes them available to the LangChain agent.

Standard input/output communication is used instead of exposing the local MCP server through a separate HTTP endpoint.

### 5. Policy-Analysis Skill

**File:** `backend/skills/policy_analysis.md`

The skill contains instructions that guide the agent in producing a balanced policy analysis.

It encourages consideration of:

- Feasibility and implementation requirements.
- Equity and accessibility.
- Privacy and voluntary participation.
- Cultural acceptability.
- Workload and opportunity costs.
- Safeguarding and professional referral access.
- Benefits, trade-offs and uncertainty.
- Evaluation metrics and evidence gaps.

The backend reads this Markdown file and incorporates its contents into the agent's system prompt. The skill is an instruction resource, not a separate AI agent.

### 6. Middleware and Guardrails

The implementation uses FastAPI CORS middleware to permit requests from the configured local frontend origins.

Pydantic validates the incoming request, including the question's minimum and maximum length.

The system prompt provides additional behavioural safeguards: the agent must not claim that mindfulness cures mental illness, invent statistics or citations, or present general wellbeing activities as substitutes for professional care.

These are application-level safeguards, not a guarantee that every generated response will be correct or safe.

## Evidence Catalogue

The MCP server contains five predefined source entries. The tool searches their titles, topic keywords and summaries.

| Source | Intended use |
|---|---|
| [WHO Guidelines on Mental Health at Work (2022)](https://www.who.int/publications/i/item/9789240053052) | Organisational factors, manager and worker training, and workplace mental-health support |
| [WHO World Mental Health Report (2022)](https://www.who.int/publications/i/item/9789240049338) | Public mental-health systems, prevention and access to services |
| [WHO: Doing What Matters in Times of Stress](https://www.who.int/publications/i/item/9789240003927) | General stress-management education and self-help skills |
| [WHO/UNESCO: Making Every School a Health-Promoting School](https://www.who.int/publications/i/item/9789240025073) | Whole-school approaches, institutional support and referral pathways |
| [NICE: Depression in Adults—Treatment and Management](https://www.nice.org.uk/guidance/ng222) | Clinical guidance that helps distinguish general wellbeing activities from treatment for depression |

### Retrieval method

The evidence-search tool uses a basic keyword-scoring approach:

1. Splits the query into words.
2. Converts words to lowercase and removes selected punctuation.
3. Excludes words with three characters or fewer.
4. Counts the query words appearing in each entry's title, topics and summary.
5. Sorts matching entries by their scores.
6. Returns up to four matches.

If no entries match, the tool returns the first three catalogue entries.

This approach is lightweight and suitable for demonstrating tool calling. It is not a semantic search engine, a live web search system or a systematic literature review.

## Installation and Setup

### Prerequisites

Install the following before running the application:

- Python compatible with the installed backend dependencies.
- Node.js and npm.
- Git.
- A Groq API key.

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/mindwell-policy-advisor.git
cd mindwell-policy-advisor
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Set up the backend

Open a terminal in the project root:

```bash
cd backend
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

For Windows Command Prompt:

```bat
.venv\Scripts\activate.bat
```

Install the dependencies listed in `backend/requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

Create the local environment configuration as described below.

### 3. Set up the frontend

Open a second terminal in the project root:

```bash
cd frontend
npm install
npm install marked dompurify
```

If the project already declares `marked` and `dompurify` in `package.json`, the first `npm install` should install them; the additional install command is included to reflect the setup used during development.

## Environment Configuration

Create a file named `.env` inside the `backend` directory.

```dotenv
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-120b
```

Replace the placeholder with your actual Groq API key. Use a model identifier supported by your Groq account and the installed integration.

**Security requirements:**

- Never commit `backend/.env`.
- Never expose your API key in screenshots, documentation or public code.
- Keep `.env` files excluded through `.gitignore`.
- Commit an `.env.example` only if it contains placeholders, never real credentials.

The `GROQ_MODEL` value above is an example of the model configuration used during development; it can be changed to another compatible model.

## Running the Application

Run the backend and frontend in separate terminals.

### Terminal 1: Backend

```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

The API should be available at:

- API health check: `http://127.0.0.1:8000/api/health`
- Interactive API documentation: `http://127.0.0.1:8000/docs`

A successful health check should return a JSON response indicating the backend status and configured framework.

The health endpoint checks whether the API key environment variable exists. It does not independently verify successful LLM inference or MCP tool execution.

### Terminal 2: Frontend

```bash
cd frontend
npm run dev
```

Open the local URL printed by the frontend development server, usually:

`http://localhost:5173`

Enter a policy question, select the target population and geographic context, and submit the request.

The backend will initialise the agent and MCP connection when processing the policy request.

## API Endpoints

### `GET /api/health`

Checks whether the backend is running and whether the Groq API key environment variable is configured.

Example response:

```json
{
  "status": "ok",
  "llm_configured": true,
  "framework": "LangChain create_agent",
  "mcp": "FastMCP stdio"
}
```

A configured key does not necessarily mean that the external model service is reachable.

### `POST /api/policy`

Generates a policy brief.

Example request:

```json
{
  "question": "How can a college introduce a student wellbeing programme?",
  "population": "College students",
  "context": "India"
}
```

The response contains fields such as:

- `answer`: the generated policy brief.
- `tool_used`: an indicator derived from the agent's returned messages.
- `model`: the configured model name.
- `evidence_sources`: the source links returned by the backend.
- `limitations`: known limitations communicated to the user.

**Implementation note:** The current `evidence_sources` list in the API response is hard-coded. It should not be interpreted as a verified list of the exact sources retrieved for an individual report. Similarly, `tool_used` is a useful indicator, not a complete audit trail.

## Example Use Case

**Policy question:**

*How can a college in India implement a practical student mental wellbeing programme without creating additional academic pressure?*

**Population:** College students  
**Geographic context:** India

The generated policy brief is organised under the following headings:

1. Executive recommendation
2. Options and rationale
3. Evidence and links
4. Implementation plan
5. Benefits and trade-offs
6. Risks, safeguards and equity
7. Evaluation metrics
8. Evidence gaps

The brief may consider optional stress-management education, accessible counselling, workload review, staff awareness, referral arrangements and pilot evaluation.

These are policy options for consideration, not automatically validated recommendations. Their suitability requires local consultation, assessment of available resources and verification of the supporting evidence.

## Responsible AI and Safeguards

MindWell Policy Advisor is intended to support policy exploration, not replace professional judgement.

The design emphasises the following principles:

- **Evidence awareness:** Encourage retrieval of the available evidence before making evidence-based claims.
- **Transparency:** Include source links, caveats and evidence gaps in the generated brief.
- **Non-clinical scope:** Do not diagnose conditions or prescribe treatment.
- **No cure claims:** Do not present mindfulness or stress-management sessions as cures for mental illness.
- **Professional support:** Treat wellbeing activities as complementary to appropriate professional care.
- **Equity:** Consider access barriers, disability inclusion, different cultural contexts and participation needs.
- **Privacy:** Avoid requesting unnecessary personal or sensitive information.
- **Voluntary participation:** Avoid coercive participation in wellbeing activities.
- **Institutional responsibility:** Consider academic workload, staff capacity and institutional conditions rather than focusing only on individual coping.
- **Human review:** Require decision-makers to verify evidence and assess local feasibility before implementing a policy.

## Limitations

1. **No live web retrieval:** It cannot discover new sources or automatically check whether existing guidance has changed.
2. **Basic keyword matching:** Retrieval is based on word overlap rather than semantic similarity.
3. **No persistent conversational memory:** The backend does not explicitly store conversation history across separate requests.
4. **No local impact estimates:** The catalogue does not provide a validated budget or estimate of intervention effectiveness for a particular institution.
5. **Not a clinical tool:** The application has not been validated for diagnosis, treatment or clinical decision-making.

## Future Improvements

Potential improvements include:

- Expand the evidence catalogue and establish a regular source-review process.
- Record the exact sources retrieved for every report.
- Improve retrieval with semantic search and a vector database.
- Add source-level relevance scores and stronger citation verification.
- Introduce automated tests for tool retrieval, API validation and report generation.
- Evaluate output quality using a defined rubric for factuality, relevance, feasibility, equity and citation accuracy.
- Add human review and feedback mechanisms.
- Support locally relevant evidence, institutional consultations and validated costing.
- Improve privacy controls, error handling, logging and deployment security.
- Add persistent conversation state only where it is useful and appropriate.

## Project Structure

The main components are organised as follows:

```text
mindwell-policy-advisor/
├── backend/
│   ├── app/
│   │   └── main.py
│   ├── skills/
│   │   └── policy_analysis.md
│   ├── mcp_server.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   ├── package.json
│   └── ...
├── .gitignore
└── README.md
```

The exact frontend files and any additional backend files depend on the current repository contents. Local secrets and generated dependency folders should not be committed.

## Learning Outcomes

This project provides practical experience with:

- Building a tool-using agent using LangChain `create_agent`.
- Integrating a hosted LLM through Groq.
- Exposing Python functionality through FastMCP.
- Connecting MCP tools to an agent through an MCP client adapter.
- Guiding agent behaviour through a Markdown-based skill.
- Building API endpoints with FastAPI and validating requests using Pydantic.
- Connecting a frontend to an AI backend.
- Rendering generated Markdown safely in a web interface.
- Identifying evidence-quality limitations, hallucination risks and responsible-AI considerations.
- Translating a broad policy question into a structured decision-support workflow.

## Disclaimer

MindWell Policy Advisor is an educational prototype developed for academic demonstration. It does not provide medical advice, diagnosis or treatment recommendations. Its generated policy briefs require independent source verification, local stakeholder consultation and human review before use in real-world decisions.

The presence of a source in the curated catalogue does not imply that the source endorses every recommendation generated by the application. The project is not affiliated with or endorsed by WHO, UNESCO, NICE or the article's author.
