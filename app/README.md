# ops-exercise
BigPanda Exercise for Ops Engineers.

Tested on Nodejs v8.9.0
## Running Instructions

```
npm install

npm start
```

HTTP server listens on port 3000

## App Healthcheck

For the app healthcheck navigate to the following url: http://\<host\>:3000/health

This would return a 200 (Ok) healthcheck response in a JSON format. In cases where the healthcheck is bad, the response would be the same JSON format with a 500 (Internal Server Error) response.
