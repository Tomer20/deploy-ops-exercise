# deploy-ops-exercise

Script for docker-compose deployment.

### Usage:
Simply run the `deploy.py` script, no requirements are needed.
Output will be written to `deploy.log` in the same directory.

### The script will:
- download .tar.gz file (if not exists) from given url.
- extract its content to app/public/images/
- run `docker-compose build` (this will rebuild the images, just in case the code/Dockerfile has changed).
- run `docker-compose down` - stop all docker-compose services and containers.
- run `docker-compose up -d` for running docker-compose in the background.
- perform health check to the deployed application.

Tested on python 3.6.0
