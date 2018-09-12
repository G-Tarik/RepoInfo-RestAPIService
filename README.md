### RESTFul API service providing repository information

#### Table of Contents
1. [Usage](#markdown-header-usage)
2. [Deployment](#markdown-header-deployment)
3. [Testing application](#markdown-header-testing)

#### Usage

`http://<server addres>:<port>/<endpoint>/<parameters>`

Github API authentication token may be included in request with header "Authorization" the same way as for direct usage of github API.
>Example: `curl -H "Authorization: token <your_token_here>" http://localhost:7000/github/rate_limit`  

Another way is to put token key inside **github_token.key** file. Please, read instructions in [github_token.key.example](github_token.key.example)


**List of endpoints:**

Endpoint:
`'/'`  
Description: Show list of all endpoints.  
Method: GET  
Parameters: None.  
Response:
```json
{
  "root_api.endpoints_list": "http://localhost/",
  "github_api.rate_limit": "http://localhost/github/rate_limit",
  "github_api.repository": "http://localhost/github/repositories/<owner>/<repo_name>"
}
```

Endpoint: `'/github/repositories/<owner>/<repo_name>'`  
Description: Show repository information.  
Method: GET  
Parameters:
> * owner - user name of repository owner
> * repo_name - name of repository  

Response:

```json
{
  "fullName": "octocat/Hello-World",
  "description": "My first repository on GitHub!",
  "cloneUrl": "https://github.com/octocat/Hello-World.git",
  "stars": 1453,
  "createdAt": "2011-01-26"
}
```

Endpoint: `'/github/rate_limit'`  
Description: Show rate limits.  
Method: GET  
Parameters: None  
Response:
```json
{
  "limit": 60,
  "remaining": 39,
  "reset": 1534590152
}
```

#### Deployment
>Please check [requirements](requirments.txt).
  
One of the possible variants is to deploy in docker container.  
In this repository there are available [Dockerfile](Dockerfile)   
and scripts for building image ([docker_build.sh](docker_build.sh))   
and running container ([docker_run.sh](docker_run.sh)).
Edit those files according to your infrastructure (change port etc.) 

[run_flask.py](run_flask.py) - creates Flask application object and runs it with Flask built in server.    
[run_gunicorn.sh](run_gunicorn.sh) - run application with gunicorn server; this script is copied to docker image and runs application in the container.


#### Testing
Requirements: [pytest](https://docs.pytest.org/en/latest/)
##### End to end test
For testing with Github API token put the token into the file `test/github_token.key` in format "token <your_token_here>".  
`pytest -v test_end2end.py` - run end-to-end tests.

##### Unit tests
run [test_github_units.py](tests_unit/test_github_units.py)
For more information please read tests [README](tests_unit/README.md)
##### Performance test
[test_server_load.sh](test/test_server_load.sh) will run load test against running application using [Siege](https://linux.die.net/man/1/siege) tool   
(siege must be installed via standard way in Linux environment).    
Description of used **siege** parameters:
> * **-c 20**  -  number of concurrent users
> * **-r 1**   - number of times to repeat the test
> * **-b**     - no delays between requests
