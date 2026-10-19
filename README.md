# RobotCasino

This project is abandoned. The last commit, on 14 June 2026, is “last changes before reworking this project.” That rework is not in this tree. The repository has no license file.

RobotCasino is a single-session scraper. A Docker image starts Chromium, opens one casino game, injects page scripts, and leaves the process in the foreground. `docs/about.md` describes a different product: a client-facing service with a Telegram bot, live status, statistics, and screenshots. That service is not implemented here. The same page says the intended service would conflict with casino terms of service.

## What is wired up

The CLI is Typer. The package is `robotcasino-robot` 1.0.0 (`src/pyproject.toml`), and the console script is `robotcasino`.

```bash
robotcasino run <browser> <casino> <game> <strategy> [--KEY value ...]
```

Browsers (`safe-resource-chrome`, `no-constraints-chrome`) are independent of the casino. These are the casino/game/strategy names the code accepts:

| Casino | Game | Strategy argument | What the code does |
| --- | --- | --- | --- |
| `one-win` | `aviator` | `simple-strategy` | Opens 1win Aviator (`https://1win.com/casino/play/v_spribe:aviator`), sets the `1w_token` cookie from `--SESSION_TOKEN`, selects USD, and injects scripts. The strategy logs new payout text. It does not place bets. |
| `mystake` | `dino` | `simple-strategy` | Sets an `AppAuth` cookie from `--SESSION_TOKEN` and opens a Mystake game URL. The strategy has no scripts. |
| `test` | `aviator` | `simple-strategy` | Opens `https://blankslate.io/`. Its script paths do not match the files under `src/data/games/test/scripts/`. |

`safe-resource-chrome` is a reduced Chromium profile. About once a minute it reads cgroup memory and restarts the browser when usage reaches `MEMORY_RELOAD_RATIO` times the limit. `no-constraints-chrome` skips that check. Both look for the browser at `/usr/bin/chromium-browser`. `HEADLESS` defaults to `1` (headless). Any other value, including `0`, shows a window.

Extra `--KEY value` arguments are stored as metadata and substituted into `src/core/domain/games/scripts/config.js`. The placeholders there are `IS_TESTING`, `FAKE_AMOUNT`, `STOP_LOSS`, `STOP_LOSS_TRIES`, and `AUTO_CASHOUT`. A placeholder with no matching argument becomes the string `false`. The Aviator simple strategy never reads `Config`.

Paths are fixed for the image: application root `/app`, screenshots `/app/screenshots/`, control socket `/tmp/robotcasino/.robotcasino.socket`, logs `/home/jhon/.cache/robotcasino/logs/messages.log` and `errors.log`. The image user is `jhon`.

## Run it

Build from the repository root. The image is `python:3.14-alpine` with the Alpine `chromium` package. `src/pyproject.toml` requires Python `>= 3.10.12`.

```bash
docker build . -t robotcasino:latest
```

Headless 1win session, using the flags from `scripts/init.sh`. Replace the token. Do not commit a live one. The checked-in helper scripts already contain a token, and `scripts/init.sh` ends with a trailing backslash, so run the command below rather than that file as-is.

```bash
mkdir -p ./output/screenshots
docker run --name robotcasino -d \
  -v ./output/screenshots/:/app/screenshots/ \
  -e HEADLESS=1 \
  -e MEMORY_RELOAD_RATIO=0.98 \
  -e MEMORY_LIMIT_MB=500 \
  --memory 800mb \
  --memory-swap 800mb \
  --shm-size=2gb \
  robotcasino:latest run \
    safe-resource-chrome one-win aviator simple-strategy \
    --SESSION_TOKEN <session-token>
```

`MEMORY_RELOAD_RATIO` is required once the low-memory browser can read both usage and a limit; otherwise that check raises. `MEMORY_LIMIT_MB` overrides the cgroup limit. `scripts/no-constraints.sh` is the same shape with `no-constraints-chrome`, `MEMORY_RELOAD_RATIO=0.95`, and `MEMORY_LIMIT_MB=700`.

For a visible browser, set `HEADLESS=0` and give the container a display. The previous copy of this file installed an X server and pointed Chromium at the host:

```bash
# Ubuntu
sudo apt install xorg
# Fedora
sudo dnf install xorg-x11-server-Xorg
# Arch Linux
sudo pacman -S xorg-server

export DISPLAY=host.docker.internal:0
```

and added `-v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=host.docker.internal:0 -e HEADLESS=0` to `docker run`. The Python code never reads `DISPLAY`; Chromium does. `scripts/init.sh` and `scripts/no-constraints.sh` both set `HEADLESS=1`.

`status`, `stop`, and `screenshot` connect to the Unix socket, so they have to run inside the same container:

```bash
docker exec robotcasino robotcasino status
docker exec robotcasino robotcasino screenshot
docker exec robotcasino robotcasino screenshot name.jpg
docker exec robotcasino robotcasino stop
docker logs robotcasino
```

`screenshot` writes a JPEG under `/app/screenshots/`. With no name it uses the container clock (`YYYY-MM-DD_HH-MM-SS.jpg`). `stop` asks the scraper to exit. `scripts/kill.sh` stops and removes the container. `scripts/screenshot.sh` runs the screenshot command. `scripts/log.sh` prints `docker logs` (follow with `-f` or `--follow`).

There is no host-install path. The directory constants assume this image.

## Layout

- `src/application` — process entrypoint
- `src/core` — scraper, CLI, base types, shared page scripts
- `src/data` — browsers, casinos, games, strategies
- `src/infrastructure` — directories, logging, socket IPC, cgroup memory
- `scripts/` — local Docker helpers
- `docs/about.md` — original goals
- `docs/architecture/docker.md` — short note that sessions were meant to run under Docker

## Gaps

No test suite and no CI workflow are in the repository. Nothing here was executed while writing this file, so the image build, the Chromium binary path on Alpine, and a live casino session are unverified.
