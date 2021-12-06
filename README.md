---
# Swagger Dagger <img src=s_d_logo.svg width=300 align=left>
### Automate API Security Testing
---
##### Swagger is used to help expose your API to developers. 
##### Swagger Dagger is used to check if your API exposes you.
###### Project Status: Infancy (started 11/29/2021)
---
#### Requirements
- Python 3.10 or newer
- Attempting to use this in versions <3.10 will likely fail due to multiple uses of the match statement

#### Background
My last project needed to test a couple hundred API endpoints for Access Permissions.
After spending a few hours looking through the source code and gathering the parameters for each endpoint, I realized this was going to take too long. 
I found a Swagger json endpoint (awesome tool for devs, even more awesome for security researchers :D).

Swagger Dagger was born.

Work In Progress
---
#### Workflow is something like this

1. Ingest the swagger json API (done)
2. Identify API http methods (done)
3. Identify API http parameters (done)
4. Interact with the APIs to identify which do not require authentication (done)
5. Fuzz the available parameters (in progress)
