# gstreamer-benchmarks


## Usage

```
./run_tests.py -h
usage: run_tests.py [-h] [-t TEST_LIST] [-l]

optional arguments:
  -h, --help            show this help message and exit
  -t TEST_LIST, --test-list TEST_LIST
                        csv-separated list of tests to run, defaults to All
  -l, --list-tests      list all available tests
```

## List available tests

```
./run_tests.py -l
Available tests:
	tests/encoding-i420.py
	tests/encoding-nv12.py
	tests/encoding-yuy2.py
	tests/glimagesink_bench.py
	tests/v4l/scaling.py
	tests/v4l/polling.py
	tests/v4l/default_caps.py
	tests/v4l/first_N_buffers.py
	tests/v4l/capture_without_input.py
	tests/v4l/first_buffer_time.py
```

## Running selective tests

```
./run_tests.py -t tests/encoding-i420.py,tests/encoding-nv12.py
```
