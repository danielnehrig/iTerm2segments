![travis](https://travis-ci.com/danielnehrig/iTerm2segments.svg?branch=master) ![iTermBadge](https://img.shields.io/badge/iTerm2-statusline-green?logo=apple&iTerm2=statusline) ![spotifyBadge](https://img.shields.io/badge/segment-itunes-green?logo=apple&segment=iTunes) ![spotifyBadge](https://img.shields.io/badge/segment-spotify-green?logo=spotify&segment=spotify)

# iTerm2 Spotify + iTunes Status Line Segments

## Install
To install, get the repo contents via the shell, and then actually install the component via iTerm2.

### Shell Install

```sh
git clone https://github.com/danielnehrig/iTerm2segments
cd iTerm2segments
./install.py
```

### iTerm2 Install

- Open iTerm2
  - If needed, install the Python runtime via the `Scripts` menu. The `spotify.py` and `iTunes.py` files should be checked under the `AutoLaunch` submenu of `Scripts`.
  - Go to Profiles > Open Profiles
  - Click Edit Profiles
  - Go to Session
  - Check Statusbar enabled
  - Then Click Configure Status Line
  - Drag the iTunes or spotify segment to active segments

![player segment](https://raw.githubusercontent.com/danielnehrig/iTerm2segments/master/itunes.png)
