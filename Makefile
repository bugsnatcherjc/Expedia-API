run:
	uvicorn app.main:app --reload

test:
	pytest -v

docker:
	docker build -t expedia-inspired . && docker run -p 8000:8000 expedia-inspired