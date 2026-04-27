# Agentic Career Coach (ACC)

This repository contains the multi-agent backend structure for the capstone project. The system is designed around a Supervisor-Specialist agent pattern, an MCP server layer, and Cloud Firestore for internship pipeline persistence.

## Project Overview

The Agentic Career Coach helps manage an internship search workflow. The intended system flow is:

1. The user sends a request to the Lead Orchestrator
2. The Lead Orchestrator performs prompt-based routing
3. If backend work is needed, it delegates the request to the Career Specialist
4. The Career Specialist calls the MCP server
5. The MCP server runs tools such as `fetch_jobs` or `sync_pipeline`
6. `sync_pipeline` reads from or writes to Cloud Firestore
7. Results move back up through the system to the user

## Current Repository Scope

This repository currently includes:

- MCP server code
- `fetch_jobs` tool using mock job data
- `sync_pipeline` tool using Cloud Firestore
- starter agent definitions and system documentation
- local run instructions for testing

## Folder Structure ( Used AI to write this part cleanly and easy to follow)

```text
agentic-career-coach/
│
├── agents/
│   ├── orchestrator.txt
│   └── specialist.txt
│
├── data/
│   └── mock_jobs.json
│
├── docs/
│   ├── firestore-schema.md
│   ├── logging-guide.md
│   └── system-flow.md
│
├── logs/
│
├── mcp_server/
│   ├── main.py
│   ├── rpc_handlers.py
│   ├── schemas.py
│   └── tool_registry.py
│
├── services/
│   ├── firestore_client.py
│   ├── jobs_service.py
│   └── pipeline_service.py
│
├── .gitignore
├── requirements.txt
└── README.md
```
## How to Run the System (Demo Instructions)

Open - https://acc-mcp-server-134991748283.us-east1.run.app/docs
Find - POST /agent/run
Paste the following - replace the word string withing the "" with the following "Find software engineering internships and save one to my pipeline."
Click execute
The following happens:
User Request
- Lead Orchestrator (Orchestrator Agent)
- Career Specialist (Worker Agent)
- MCP Server (/sse endpoint)
- Firestore (pipeline persistence)
- Final Response returned to user
Then go to your google cloud account with your VCU email (you have been added as the editor). Search for the Cloud Run then click on acc-mcp-server and open Logs. You will see the following:
[AGENT-RUN]
[ORCHESTRATOR]
[SPECIALIST]
[MCP-SSE]
[FETCH_JOBS]
[FIRESTORE]
What it does is, it demostrates Agent-to-Agent delegation (A2A), JSON-RPC over SSE (MCP), Backend tool execution, Data persistence.
After that you can search for Firestore and click on internship_pipeline. You will see saved internship records created by the agent system.
