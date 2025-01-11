> [!WARNING]
> **ARCHIVED REPOSITORY**
>
> This project is deprecated, and this repository is available only for
> archiving purposes. I am also no longer maintaining the associated Docker
> image, which is probably wildly outdated by now.

# Quick reference

* **Maintained by:** [taskbjorn](https://github.com/taskbjorn)

* **Where to get help:** [GitHub](https://github.com/taskbjorn/docker-kf2ds/issues)

# Supported tags and respective Dockerfile links

* [**docker-kf2ds**](https://github.com/taskbjorn/docker-kf2ds/blob/main/build)
  * [`stable`](https://github.com/taskbjorn/docker-kf2ds/blob/main/build/stable)

# What is `docker-kf2ds`?

`docker-kf2ds` is a Docker container for the Killing Floor 2 dedicated server.

![docker-kf2ds.png](https://github.com/taskbjorn/docker-kf2ds/blob/main/docker-kf2ds.png)

The container is based on a minimal Debian image running SteamCMD.

# How to use this image

## Basic setup using Docker Compose

> [!IMPORTANT]
> When running the server for the first time, use the script `firstrun.sh`. This
> will create the required Docker volumes for you and set permissions
> accordingly.

Below is a Docker Compose template saving custom maps permanently and using
[Magicked](https://github.com/th3-z/kf2-magicked-admin).

```yml
networks:
  backend:
    name: kf2ds
  proxy:
    external: true

services:
  server:
    container_name: kf2ds_server
    env_file:
      - env/kf2ds-server.env
    image: taskbjorn/docker-kf2ds:latest
    networks:
      - backend
      - proxy
    ports:
      - "7777:7777/udp"
      - "27015:27015/udp"
    restart: unless-stopped
    volumes:
      - webserver:/home/kf2/.kf2ds/server/KFGame/Web/ServerAdmin/:ro
      - overrides:/home/kf2/.kf2ds/overrides/kf2/KFGame/Cache/:ro

  magicked:
    container_name: kf2ds_magicked
    env_file:
      - env/kf2ds-magicked.env
    image: th3z/kf2-magicked-admin:latest
    networks:
      - backend
    restart: unless-stopped
    volumes:
      - ./magicked/magicked_admin.conf:/magicked_admin/conf/magicked_admin.conf:ro
      - ./magicked/scripts/:/magicked_admin/conf/scripts:ro
      - webserver:/mnt/kf2ds-server/KFGame/Web/ServerAdmin/

volumes:
  magicked:
    name: kf2ds_magicked
  overrides:
    name: kf2ds_overrides
  webserver:
    name: kf2ds_webserver
```

## Environment variables

* `ADMIN_PASSWORD`  
  Password for the default WebAdmin user (username Admin). Defaults to a random
  32 character alphanumeric password.

* `USER_USERNAME`  
  Username for the less privileged user. Defaults to `user`.

* `USER_PASSWORD`  
  Password for the less privileged user. Defaults to a random 32 character
  alphanumeric password.

* `USER_DISPLAYNAME`  
  Display name (used in chat) for the less privileged user.

* `BOT_USERNAME`  
  Username for the Magicked bot. Defaults to `magibot`.

* `BOT_PASSWORD`  
  Password for the Magicked bot. Defaults to a random 32 character alphanumeric
  password.

* `BOT_DISPLAYNAME`  
  Display name (used in chat) for the Magicked bot. Defaults to `Magibot`.

* `GAME_DIFFICULTY`  
  Game difficulty at server startup. Defaults to `3` (Hell on Earth).
   * 0 - Normal
   * 1 - Hard
   * 2 - Suicidal
   * 3 - Hell on Earth

* `GAME_LENGTH`  
  Game length at server startup. Defaults to `1` (7 waves).
   * 0 - Short (4 waves)
   * 1 - Medium (7 waves)
   * 2 - Long (10 waves)

* `GAME_PASSWORD`  
  Password to join the game. Defaults to empty (no password).

## Server startup process

On server startup, the configuration overrides specified for
`LinuxGame-KFGame.ini` are merged into the default file. The custom maps
specified in the `kf2ds-cmaplist.json` dictionary are added to the workshop
subscription, inserted in the WebAdmin entries and added into a second maplist
(which is set as default). It might take a significant amount of time for the
maps to be downloaded and occasionally a server restart may be required to
complete all downloads: this is a limitation of the Killing Floor 2 Linux
dedicated server and not of this specific Docker image.

## Persistent storage

If you would like to avoid downloading custom maps at each server start, you may
choose either of these solutions:

1. Mount two separate volumes: `kf2ds-cache` pointed to
   `/home/kf2/.kf2ds/server/KFGame/Cache` and `kf2ds-workshop` pointed to
   `/home/kf2/.kf2ds/server/Binaries/Win64/steamapps/workshop`.

2. Mount a single `kf2ds-server` volume pointed to `/home/kf2/.kf2ds/server`.
   This is the preferred approach if you are planning to use
   [Magicked](https://github.com/th3-z/kf2-magicked-admin), as you will be able
   to mount the same volume on the Magicked container to allow for WebAdmin
   patching.

# License

This image is licensed under [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)

As with all Docker images, these likely also contain other software which may be
under other licenses (such as Bash, etc from the base distribution, along with
any direct or indirect dependencies of the primary software being contained).

As for any pre-built image usage, it is the image user's responsibility to
ensure that any use of this image complies with any relevant licenses for all
software contained within.
