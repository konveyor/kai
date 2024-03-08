run-postgres:
	docker run -it -v data:/var/lib/postgresql/data -e POSTGRES_USER=kai -e POSTGRES_PASSWORD=dog8code -e POSTGRES_DB=kai -p 5432:5432 docker.io/pgvector/pgvector:pg15

run-server:
	python ./kai/server.py

