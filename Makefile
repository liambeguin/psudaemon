setup:
	@poetry install

run:
	@poetry run psudaemon

fix:
	@poetry run ruff check psudaemon/*/*.py  --fix

start-prometheus:
	@podman run --rm \
		--security-opt label=disable \
		-p 9090:9090 \
		--network=host \
		-v ./monitoring/prometheus.yaml:/etc/prometheus/prometheus.yml \
		quay.io/prometheus/prometheus

prometheus-reload:
	@podman exec prometheus killall -HUP prometheus

start-exporter:
	@podman run --rm \
		--security-opt label=disable \
		-p 7979:7979 \
		--network=host \
		--workdir / \
		-v ./monitoring/json_exporter.yaml:/config.yml \
		quay.io/prometheuscommunity/json-exporter
