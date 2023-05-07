docker-build:
	docker build . -t xorus/pointypoints:test
	docker push xorus/pointypoints:test
