System flow

1. User sends request to Lead Orchestrator
2. Lead Orchestrator performs prompt-based routing
3. If tool/data work is needed, it delegates to Career Specialist
4. Career Specialist calls MCP Server
5. MCP Server runs fetch_jobs or sync_pipeline
6. MCP Server reads from or writes to Cloud Firestore
7. Result returns to Career Specialist
8. Career Specialist returns result to Lead Orchestrator
9. Lead Orchestrator returns final response to User
