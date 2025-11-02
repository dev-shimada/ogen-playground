# api
## generate
```bash
go generate ./...
```


curl -X GET 'http://localhost:8080/v3/pet/10'


curl 'http://localhost:8080/v3/pet' --json '{"id": 10,"name": "doggie","photoUrls": ["string"],"status": "available"}'
