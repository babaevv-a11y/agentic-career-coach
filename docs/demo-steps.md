## All THE STEPS WERE CREATED WITH THE HELP OF CHATGPT USING MY NOTES AND MY COMMENTS AND SUBMISSION DETAILS FOR THE CLEAN LOOK

## AND CLEAN PATH FOR THE GROUPMATE TO FOLLOW

# Demo and Testing Guide (Step-by-Step)

This guide shows exactly how to open the project and start the backend server.

# 1. Open the GitHub Repository

Click this link:

https://github.com/babaevv-a11y/agentic-career-coach

From here:

- Click **README.md** to understand the project
- Open folders:
  - `mcp_server` - backend logic (MCP server)
  - `services` - Firestore and tool logic
  - `docs` - explanations and flow

# 2. Open the project in VS Code

If running locally:

1. Open VS Code
2. Click **File then Open Folder**
3. Select the folder:

agentic-career-coach

# 3. Open terminal in VS Code

Top menu:

- Click **Terminal**
- Click **New Terminal**

# 4. Set Firestore credentials (VERY IMPORTANT)

In the terminal (PowerShell), run:

$env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\vladi\Desktop\VCU masters degree\Spring 2026\Data Communications INFO 520\agentic-career-coach\gcp-key.json"

IMPORTANT:

- This must be ONE LINE ( I mean it)
- You must run this every time you open a new terminal

---

# 5. Start the backend server

Run this command:

python -m uvicorn mcp_server.main:app --reload

If successful, you will see:

Uvicorn running on http://127.0.0.1:8000

---

# 6. Open the backend testing page (Swagger UI)

Open this link in your browser:

http://127.0.0.1:8000/docs

This page allows you to test all backend functionality.

---

# 7. Test fetch_jobs

In Swagger:

1. Find **POST /rpc**
2. Click **Try it out**
3. Paste this request:

{
"jsonrpc": "2.0",
"method": "fetch_jobs",
"params": {
"role": "Intern"
},
"id": 1
}

4. Click **Execute**

Expected result:

- A list of job results should be returned

---

# 8. Test sync_pipeline (CREATE)

Paste this request:

{
"jsonrpc": "2.0",
"method": "sync_pipeline",
"params": {
"action": "create",
"job_id": "1",
"company": "Google",
"title": "Software Engineer Intern",
"location": "Remote",
"url": "https://careers.google.com",
"status": "saved",
"notes": "Demo entry",
"deadline": "2026-05-01"
},
"id": 2
}

Click **Execute**

IMPORTANT:

- Copy the `document_id` from the response

---

# 9. Test sync_pipeline (LIST)

Paste this request:

{
"jsonrpc": "2.0",
"method": "sync_pipeline",
"params": {
"action": "list"
},
"id": 3
}

Click **Execute**

Expected result:

- All pipeline entries should be displayed

---

# 10. Test sync_pipeline (UPDATE STATUS)

Replace document_id with the real value from Step 8:

{
"jsonrpc": "2.0",
"method": "sync_pipeline",
"params": {
"action": "update_status",
"document_id": "PASTE_REAL_ID_HERE",
"status": "applied"
},
"id": 4
}

Click **Execute**

Expected result:

- Status is updated successfully

---

# 11. Verify data in Firestore

Open this link:

https://console.cloud.google.com/firestore

Then:

1. Log in using your VCU email
2. At the top of the page, click the project selector
3. Select the project:

agentic-career-coach

(You should see the project since I added both the groupmate and the professor as the editors)

4. In the left panel, click:
   Firestore Database

5. Click the collection:

   internship_pipeline

You should now see:

- documents created from the demo
- fields such as job_id, company, status, etc.
- updated status after running the update step

---

# 12. Check terminal logs

Go back to VS Code.

Look at the terminal where the server is running.

You should see logs like:

[MCP] Incoming RPC request
[SYNC_PIPELINE] Action requested
[FIRESTORE] sync_pipeline request completed

These logs show how the request moved through the backend.

---

# 13. Required screenshot (for submission)

Take a screenshot that includes:

- terminal logs
- at least one sync_pipeline request
- proof that Firestore was used

This screenshot will be used for the "System Trace & Logs" submission.

---

# 14. Demo flow (follow exactly)

Use this order during the demo:

1. Open GitHub repository
2. Show README briefly
3. Open project in VS Code
4. Start the server
5. Open Swagger UI (http://127.0.0.1:8000/docs)
6. Run fetch_jobs
7. Run sync_pipeline create
8. Run sync_pipeline list
9. Run sync_pipeline update_status
10. Open Firestore and show data
11. Show terminal logs

---

# 15. Files to show during code review

If asked to explain the code, open these files:

mcp_server/main.py  
mcp_server/rpc_handlers.py  
mcp_server/tool_registry.py  
services/jobs_service.py  
services/pipeline_service.py  
services/firestore_client.py

Explain:

- how requests enter through /rpc
- how routing is handled
- how tools are selected
- how Firestore is used for persistence
