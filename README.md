# gstreamer-benchmarks

A python-based gstreamer benchmarking tool that currently has:
* a performance benchmark of gstreamer-vaapi, software codecs, nvenc, omx (pi & jetson)
* some v4l compliance tests
* some glimagesink benchmarks

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
## Output

Results are written to a text file (result-hostname-1476458424.txt) as a tsv (tab-separated file)

```
###########################################
####### Tests finished, results ###########
###########################################

[Pass]
Gstreamer 1.9.90: I420 Encoding benchmark, GPU: Intel Corporation Xeon E3-1200 v3/4th Gen Core Processor Integrated Graphics Controller (rev 06) CPU: Intel(R) Core(TM) i7-4771 CPU @ 3.50GHz Intel(R) Haswell Desktop
Encoder Sample  Mean fps    Min fps Max fps Mean Mpix/s Min Mpix/s  Max Mpix/s
x264enc speed-preset=ultrafast bitrate=20000 tune=zerolatency key-int-max=30    pattern=black-1920-1080-30  316 307 328 655 637 680
vaapih264enc rate-control=2 bitrate=20000 keyframe-period=30    pattern=black-1920-1080-30  154 150 159 320 311 330
```
