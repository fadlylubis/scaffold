.PHONY: build run test lint fmt hooks
build:
	go build -o bin/__PROJECT__ ./cmd/__PROJECT__
run:
	go run ./cmd/__PROJECT__
test:
	go test -race ./...
lint:
	go vet ./...
	test -z "$$(gofmt -l .)"
fmt:
	gofmt -w .
hooks:
	git init -q
	uvx pre-commit install
