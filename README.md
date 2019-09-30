# 🎵 bum

[![PyPI](https://img.shields.io/pypi/v/bum.svg)](https://pypi.python.org/pypi/bum/)
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE.md)
[![Build Status](https://travis-ci.org/dylanaraps/bum.svg?branch=master)](https://travis-ci.org/dylanaraps/bum)
[![Donate](https://img.shields.io/badge/donate-patreon-yellow.svg)](https://www.patreon.com/dyla)

`bum` is a daemon that downloads album art for songs playing in `mpd`/`mopidy` and displays them in a little window. `bum` doesn't loop on a timer, instead it waits for `mpd`/`mopidy` to send a `player` event. When it receives a `player` event it wakes up and downloads album art for the current playing track. This makes `bum` lightweight and makes it idle at `~0%` CPU usage.

`bum` uses [musicbrainz](https://musicbrainz.org/) to source and download cover art, if an album is missing it's cover art you can easily create an account and fill in the data yourself. `bum` outputs a `release-id` which you can use to find the exact entry on musicbrainz.

Note: `bum` is meant to be used with files that don't have embedded album art (`mopidy-spotify`).


![showcase](http://i.imgur.com/uKomDoL.gif)


## Dependencies

- `python 3.6+`
- `python-mpd2`
- `musicbrainzngs`

### Optional

bum supports multiple display outputs, specified using `--display {dummy,tk,mpv}`, you must install the dependencies required for your chosen output:

- `python-mpv` - for mpv output
- `python3-pil`, `python3-tk` and `python3-pil.imagetk` plus `fonts` and `font_connection` from pypi - for tk/PIL output
- `st7789` - for ST7789 1.3" 240x240 LCD output

## Installation

```sh
pip3 install --user bum
```


## Usage

```sh
usage: bum [-h] [--update-interval "i"] [--size "px"]
                   [--cache_dir "/path/to/dir"] [--version] [--port PORT]
                   [--server SERVER] [--no_display] [--display {dummy,tk,mpv}]

bum - Download and display album art for mpd tracks.

optional arguments:
  -h, --help            show this help message and exit
  --update-interval "i"
                        overlay update interval in seconds.
  --size "px"           what size to display the album art in.
  --cache_dir "/path/to/dir"
                        Where to store the downloaded cover art.
  --version             Print "bum" version.
  --port PORT           Use a custom mpd port.
  --server SERVER       Use a remote server instead of localhost.
  --no_display          Only download album art, don't display.
  --display {dummy,tk,mpv}
                        Display class to use.
```


## Donate

Donations will allow me to spend more time working on `bum`.

If you like `bum` and want to give back in some way you can donate here:

**https://patreon.com/dyla**
