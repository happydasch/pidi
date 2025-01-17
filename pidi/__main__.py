# -*- coding: utf-8 -*-
"""
   ▄███████▄  ▄█  ████████▄   ▄█
  ███    ███ ███  ███   ▀███ ███
  ███    ███ ███▌ ███    ███ ███▌
  ███    ███ ███▌ ███    ███ ███▌
▀█████████▀  ███▌ ███    ███ ███▌
  ███        ███  ███    ███ ███
  ███        ███  ███   ▄███ ███
 ▄████▀      █▀   ████████▀  █▀

Pidi - Pirate Display

A fork of "bum" originally
created by Dylan Araps
"""
import argparse
import pathlib
import time
import sys

from .display import get_display_types
from .client import get_client_types
from .control import get_control_types


from .__init__ import __version__


def get_args(display_types, client_types, control_types):
    """Get the script arguments."""
    description = "pidi - Download and display album art \
                   for mpd tracks."
    arg = argparse.ArgumentParser("pidi", description=description)

    arg.add_argument("--update-interval", metavar="\"i\"",
                     help="overlay update interval in seconds.",
                     default=1.0,
                     type=float)

    arg.add_argument("--fps",
                     help="frames per second.",
                     type=int, default=30)

    arg.add_argument("--size", metavar="\"px\"",
                     help="what size to display the album art in.",
                     default=240)

    arg.add_argument("--cache_dir", metavar="\"/path/to/dir\"",
                     help="Where to store the downloaded cover art.",
                     default=pathlib.Path.home() / ".cache/pidi",
                     type=pathlib.Path)

    arg.add_argument("--version", action="store_true",
                     help="Print \"pidi\" version.")

    arg.add_argument("--no_display",
                     action="store_true",
                     help="Only download album art, don't display.")

    arg.add_argument("--display", choices=display_types.keys(),
                     help="Display class to use.",
                     default='dummy')

    arg.add_argument("--client", choices=client_types.keys(),
                     help="Client class to use.",
                     default='mpd')

    arg.add_argument("--control", choices=control_types.keys(),
                     help="Control class to use.",
                     default='dummy')

    # Strip out --help so we can parse_known_args
    # without triggering help text output.
    has_help = False
    try:
        sys.argv.remove('--help')
        has_help = True
    except ValueError:
        pass

    args, _ = arg.parse_known_args()

    # Add display/client specific args into the parser
    display_types[args.display].add_args(arg)

    client_types[args.client].add_args(arg)

    control_types[args.control].add_args(arg)

    # Add --help back if it was supplied
    if has_help:
        sys.argv.append('--help')

    return arg.parse_args()


def process_args(args):
    """Process the arguments."""
    if args.version:
        print("pidi {version}".format(version=__version__))
        sys.exit(0)


def main():
    """Main script function."""
    display_types = get_display_types()
    client_types = get_client_types()
    control_types = get_control_types()

    args = get_args(display_types, client_types, control_types)
    process_args(args)

    if args.no_display:
        print("Warning --no_display overrides --display option!")
        args.display = 'dummy'

    display = display_types[args.display](args)

    client = client_types[args.client](args)

    control = control_types[args.control](args)
    control.set_client(client)

    last_track = ''
    last_update = 0

    while True:
        if client.update_pending() or time.time() - last_update > float(args.update_interval):
            status = client.status()
            currentsong = client.currentsong()

            control.update_controls()

            if status == {} or currentsong == {}:
                pass  # No status or song info available
            else:
                title = currentsong.get('title', 'Untitled')
                artist = currentsong.get('artist', 'No Artist')
                album = currentsong.get('album', title)
                if isinstance(title, list):
                    title = ", ".join(title)
                if isinstance(artist, list):
                    artist = ", ".join(artist)
                if isinstance(album, list):
                    album = ", ".join(album)
                current_track = f"{title} - {artist}, {album}"

                if current_track != last_track:
                    print(f"pidi: got new track: {current_track}")

                get_art = current_track != last_track or getattr(client, "pending_art", False)

                if get_art:
                    client.get_art(args.cache_dir, args.size)
                    display.update_album_art(args.cache_dir / "current.jpg")
                    last_track = current_track

                display.update_overlay(
                    status['random'] == '1',
                    status['repeat'] == '1',
                    status['state'],
                    int(status['volume']),
                    float(status.get('elapsed', 0)) / float(currentsong['time']),
                    float(status.get('elapsed', 0)),
                    title,
                    album,
                    artist
                )

                last_update = time.time()

        display.redraw()

        time.sleep(1.0 / args.fps)


if __name__ == "__main__":
    main()
