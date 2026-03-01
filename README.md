# RobotCasino


## Tutorials


### X11 and RobotCasino

To initialize RobotCasino and display the browser on GUI, you have to install [X11](https://en.wikipedia.org/wiki/X11) on your system.

#### Ubuntu

```bash
sudo apt install xorg
```

#### Fedora

```bash
sudo dnf install xorg-x11-server-Xorg
```

#### Arch Linux

```bash
sudo pacman -S xorg-server
```

Then you have to set the display variable in your system.
```bash
export DISPLAY=host.docker.internal:0
```

Finally execute the container with the following command:

```bash
docker run --name robotcasino -d -v ./output/:/app/output -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=host.docker.internal:0 -e HEADLESS=0 -e SESSION_TOKEN={session_token} robotcasino run {game} -s {strategy}
```