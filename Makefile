OS ?= ubuntu-20.04
DOCKER_IMG = gst-bench-${OS}


_build_docker_img:
	docker build -t ${DOCKER_IMG} -f docker/Dockerfile.${OS} docker/

test:
	${MAKE} _build_docker_img
	docker run \
		--rm -w /src \
		-t \
		-v ${CURDIR}:/src \
		--tmpfs /tmp \
		${DOCKER_IMG} /src/run_tests.py
