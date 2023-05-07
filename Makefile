docker-build:
	docker build . -t xorus/pointypoints:test
	docker push xorus/pointypoints:test

push-all:
	git push
	cd userscript
	git push
