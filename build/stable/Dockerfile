FROM debian:buster-slim

ENV DEBIAN_FRONTEND noninteractive

# Install SteamCMD, Python and command line tools
RUN sed -i "s#deb http://deb.debian.org/debian buster main#deb http://deb.debian.org/debian buster main contrib non-free#g" /etc/apt/sources.list && \
    sed -i "s#deb http://security.debian.org/debian-security buster/updates main#deb http://security.debian.org/debian-security buster/updates main contrib non-free#g" /etc/apt/sources.list && \
    echo steamcmd steam/question select "I AGREE" | debconf-set-selections && \
    echo steamcmd steam/license note '' | debconf-set-selections && \
    dpkg --add-architecture i386 && \
    apt-get update -qq 2> /dev/null && \
    apt-get install -o=Dpkg::Use-Pty=0 -yqq \
        ca-certificates \
        crudini \
        curl \
        lib32stdc++6 \
        lib32gcc1 \
        libcurl4 \
        libsdl2-2.0-0:i386 \
        locales \
        python3 \
        steamcmd 2> /dev/null && \
    sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8 && \
    ln -s /usr/games/steamcmd /usr/bin/steamcmd

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Create and switch to a non-privileged user, copy entrypoint script
COPY helpers/kf2ds-entrypoint.sh helpers/kf2ds-cmapshelper.py /

RUN groupadd --gid 1000 kf2 && \
    useradd --uid 1000 --gid 1000 --shell /bin/bash --create-home kf2 && \
    mkdir -p /home/kf2/.kf2ds/helpers /home/kf2/.kf2ds/overrides /home/kf2/.kf2ds/server/ && \
    mv -t /home/kf2/.kf2ds/helpers/ /kf2ds-entrypoint.sh /kf2ds-cmapshelper.py && \
    chown -R 1000:1000 /home/kf2/.kf2ds/helpers /home/kf2/.kf2ds/overrides /home/kf2/.kf2ds/server/ && \
    chmod +x /home/kf2/.kf2ds/helpers/kf2ds-entrypoint.sh

USER kf2

# Download the latest server binary and create missing cache directory, launch server to generate configuration files, enable WebAdmin, enable MultiWebAdmin, disable takeover, enable workshop redirect
RUN steamcmd +@ShutdownOnFailedCommand +login anonymous +force_install_dir /home/kf2/.kf2ds/server +app_update 232130 validate +quit && \
    mkdir -p /home/kf2/.kf2ds/server/KFGame/Cache && \
    (/home/kf2/.kf2ds/server/Binaries/Win64/KFGameSteamServer.bin.x86_64 kf-burningparis?Game=KFGameContent.KFGameInfo_Survival &) 2> /dev/null | grep -q 'DevOnline: Steam Servers Connected' && kill -- -1 && \
    crudini --set /home/kf2/.kf2ds/server/KFGame/Config/KFWeb.ini IpDrv.WebServer bEnabled true && \
    (/home/kf2/.kf2ds/server/Binaries/Win64/KFGameSteamServer.bin.x86_64 kf-burningparis?Game=KFGameContent.KFGameInfo_Survival &) 2> /dev/null | grep -q 'DevOnline: Steam Servers Connected' && kill -- -1 && \
    crudini --set /home/kf2/.kf2ds/server/KFGame/Config/LinuxServer-KFGame.ini Engine.AccessControl AdminPassword Password && \
    crudini --set /home/kf2/.kf2ds/server/KFGame/Config/KFWebAdmin.ini WebAdmin.WebAdmin AuthenticationClass WebAdmin.MultiWebAdminAuth && \
    crudini --set /home/kf2/.kf2ds/server/KFGame/Config/LinuxServer-KFEngine.ini Engine.GameEngine bUsedForTakeover false && \
    sed -i '/^DownloadManagers=IpDrv.HTTPDownload.*/i DownloadManagers=OnlineSubsystemSteamworks.SteamWorkshopDownload' /home/kf2/.kf2ds/server/KFGame/Config/LinuxServer-KFEngine.ini && \
    (/home/kf2/.kf2ds/server/Binaries/Win64/KFGameSteamServer.bin.x86_64 kf-burningparis?Game=KFGameContent.KFGameInfo_Survival &) 2> /dev/null | grep -q 'DevOnline: Steam Servers Connected'

# Run entrypoint script
WORKDIR /home/kf2/.kf2ds/server
EXPOSE 7777 27015
ENTRYPOINT /home/kf2/.kf2ds/helpers/kf2ds-entrypoint.sh

