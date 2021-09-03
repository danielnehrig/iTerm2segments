import iterm2
import sys
import os
import locale

from subprocess import Popen, PIPE
from functools import partial


def get_preferred_input_encoding():
    if hasattr(locale, 'LC_MESSAGES'):
        return (
            locale.getlocale(locale.LC_MESSAGES)[1]
            or locale.getdefaultlocale()[1]
            or 'latin1'
        )
    return (
        locale.getdefaultlocale()[1]
        or 'latin1'
    )


def get_preferred_output_encoding():
    if hasattr(locale, 'LC_MESSAGES'):
        return (
            locale.getlocale(locale.LC_MESSAGES)[1]
            or locale.getdefaultlocale()[1]
            or 'ascii'
        )
    return (
        locale.getdefaultlocale()[1]
        or 'ascii'
    )


def _convert_seconds(seconds):
    return '{0:.0f}:{1:02.0f}'.format(*divmod(float(seconds), 60))


def _convert_state(state):
    state = state.lower()
    if 'play' in state:
        return '▶'
    if 'pause' in state:
        return '▮▮'
    if 'stop' in state:
        return '▮▮'
    return 'fallback'


def run_cmd(cmd, stdin=None, strip=True):
    try:
        p = Popen(cmd, shell=False, stdout=PIPE, stdin=PIPE)
    except OSError as e:
        return None
    else:
        stdout, err = p.communicate(
                stdin if stdin is None else stdin.encode(get_preferred_output_encoding()))
        stdout = stdout.decode(get_preferred_input_encoding())
    return stdout.strip() if strip else stdout


def asrun(ascript):
    return run_cmd(['osascript', '-'], ascript)


async def main(connection):
    component = iterm2.StatusBarComponent(
            short_description="spotify",
            detailed_description="This Component shows the current spotfiy song",
            knobs=[],
            exemplar="spotify",
            update_cadence=1,
            identifier="com.iterm2.spotify")

    @iterm2.StatusBarRPC
    async def coro(
            knobs,
            rows=iterm2.Reference("rows"),
            cols=iterm2.Reference("columns")):
        status_delimiter = '-~`/='
        ascript = '''
          tell application "System Events"
            set process_list to (name of every process)
          end tell

          if process_list contains "Spotify" then
            tell application "Spotify"
              if player state is playing or player state is paused then
                set track_name to name of current track
                set artist_name to artist of current track
                set album_name to album of current track
                set track_length to duration of current track
                set now_playing to "" & player state & "{0}" & album_name & "{0}" & artist_name & "{0}" & track_name & "{0}" & track_length & "{0}" & player position
                return now_playing
              else
                return player state
              end if
            end tell
          end if
        '''.format(status_delimiter)
        spotify = asrun(ascript)
        if not spotify:
            return ""

        spotify_status = spotify.split(status_delimiter)
        state = _convert_state(spotify_status[0])
        if state == 'stop':
            return None

        artist = spotify_status[2]
        title = spotify_status[3]
        total = _convert_seconds(int(spotify_status[4].replace(',', '.'))/1000)
        elapsed = _convert_seconds(spotify_status[5].replace(',', '.'))
        return "{} {} - {} {}/{}".format(state, artist, title, elapsed, total)

    # Register the component.
    await component.async_register(connection, coro)

iterm2.run_forever(main)
