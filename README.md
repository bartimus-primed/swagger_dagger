# Swagger Dagger
### Automate API Security Testing
##### Swagger is used to help expose your API to developers. 
##### Swagger Dagger is used to check if your API exposes you.
###### Project Status: Infancy (started 11/29/2021)
---

#### Background
I accepted a new job and wanted to make sure that I didn't leave my current team in the dark. My last project needed to test a couple hundred API endpoints for Access Permissions.
After spending a few hours looking through the source code and gathering the parameters for each endpoint. I realized this was going to take too long. 
I found a Swagger json endpoint (awesome tool for devs, even more awesome for security researchers :D).

Swagger Dagger was born.

Work In Progress
---
#### Workflow is something like this

Step 1. Ingest the swagger json API (done)
Step 2. Identify API http methods (done)
Step 3. Identify API http parameters (done)
Step 4. Interact with the APIs to identify which do not require authentication (done)
Step 5. Fuzz the available parameters (in progress)
