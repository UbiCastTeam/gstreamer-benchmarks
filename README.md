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

## Adding video samples

To use actual video samples instead of generated video, just drop them into samples/ with the following filename syntax: name-width-height-framerate.mp4 (e.g. bbb-1920-1080-30.mp4), they will be added automatically; you can disable the sample auto scanning by setting SCAN_SAMPLES to False, but you can still add them to the SAMPLES variable in the actual test:

```
    e.SAMPLES = [
        'pattern=black-1920-1080-30',
		...
        'sample=mysample-1920-1080-30.mp4',
    ]
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

Results are written to a text file (result-hostname-2016-11-16-23-32.txt) as a tsv (tab-separated file)

```
###########################################
####### Tests finished, results ###########
###########################################

[Pass]
Gstreamer 1.10.0: I420 Encoding benchmark (mean fps over 1 passes), GPU: Intel Corporation 3rd Gen Core processor Graphics Controller (rev 09) CPU: Intel(R) Core(TM) i5-3230M CPU @ 2.60GHz Intel(R) Ivybridge Mobile (live mode: False)
Encoder Sample  fps +/-
x264enc speed-preset=ultrafast bitrate=20000 tune=zerolatency key-int-max=30    pattern=black-1920-1080-30-1ch  146 0
vaapih264enc rate-control=2 bitrate=20000 keyframe-period=30    pattern=black-1920-1080-30-1ch  147 0
x264enc speed-preset=ultrafast bitrate=20000 tune=zerolatency key-int-max=30    pattern=smpte-1920-1080-30-1ch  123 0
vaapih264enc rate-control=2 bitrate=20000 keyframe-period=30    pattern=smpte-1920-1080-30-1ch  137 0
x264enc speed-preset=ultrafast bitrate=20000 tune=zerolatency key-int-max=30    pattern=snow-1920-1080-30-1ch   74  0
vaapih264enc rate-control=2 bitrate=20000 keyframe-period=30    pattern=snow-1920-1080-30-1ch   144 0
```

You can also convert the result file to an ASCII-style table suitable for email/ticket inclusion:

```
./tabulate_results.py result-myhost-2016-11-16-23-32.txt 

Gstreamer 1.10.0: I420 Encoding benchmark (mean fps over 1 passes), GPU: Intel Corporation 3rd Gen Core processor Graphics Controller (rev 09) CPU: Intel(R) Core(TM) i5-3230M CPU @ 2.60GHz Intel(R) Ivybridge Mobile (live mode: False)

            Encoder                           Sample               fps    +/-
--------------------------------  ------------------------------  -----  -----
x264enc speed-preset=ultrafast..  pattern=black-1920-1080-30-1ch   146     0
vaapih264enc rate-control=2 bi..  pattern=black-1920-1080-30-1ch   147     0
x264enc speed-preset=ultrafast..  pattern=smpte-1920-1080-30-1ch   123     0
vaapih264enc rate-control=2 bi..  pattern=smpte-1920-1080-30-1ch   137     0
x264enc speed-preset=ultrafast..  pattern=snow-1920-1080-30-1ch    74      0
vaapih264enc rate-control=2 bi..  pattern=snow-1920-1080-30-1ch    144     0

Table is 77 lines wide
```

## Deps

* python >= 3.4
* gstreamer >= 1.0
* gst-plugins-base
* gst-plugins-good
* gst-plugins-ugly
* gstreamer-vaapi
* gst-libav (optional, for samples)
* python-tabulate (for the tabulate_results.py script)

nvenc (in -bad) must be compiled by hand
