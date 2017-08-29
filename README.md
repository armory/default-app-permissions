This little app, sets up default groups for your Spinnaker Fiat configuration


### First Build The Image
```
docker build -t default-app-permissions .
```

### Run the Container
```
docker run default-app-permissions https://myspinnaker.io:8084 0762f828-40c1-40af-b381-0e8c556ed1fb my-github-teamname isaac@example.org
```
