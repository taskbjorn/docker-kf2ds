#!/bin/bash

# Run custom maps helper script
printf "Running custom maps helper script\n"
python3 /home/kf2/.kf2ds/helpers/kf2ds-cmapshelper.py

# Merge configuration files
printf "Applying configuration files overrides\n"
crudini --merge  /home/kf2/.kf2ds/server/KFGame/Config/LinuxServer-KFGame.ini < /home/kf2/.kf2ds/server/Overrides/LinuxServer-KFGame.ini

# Applying environment variables configuration overrides
crudini --set /home/kf2/.kf2ds/server/KFGame/Config/LinuxServer-KFGame.ini Engine.GameInfo GameDifficulty ${GAME_DIFFICULTY}
crudini --set /home/kf2/.kf2ds/server/KFGame/Config/LinuxServer-KFGame.ini KFGame.KFGameInfo GameLength ${GAME_LENGTH}
crudini --set /home/kf2/.kf2ds/server/KFGame/Config/LinuxServer-KFGame.ini Engine.GameReplicationInfo ServerName ${SERVER_NAME}

# Change Admin user password
crudini --set /home/kf2/.kf2ds/server/KFGame/Config/KFMultiAdmin.ini "Admin MultiAdminData" Password $(echo -n "${ADMIN_PASSWORD}Admin" | sha1sum)

# Add less privileged user to WebAdmin
crudini --set /home/kf2/.kf2ds/KFGame/server/Config/KFMultiAdmin.ini "${USER_USERNAME} MultiAdminData" DisplayName ${USER_DISPLAYNAME}
crudini --set /home/kf2/.kf2ds/KFGame/server/Config/KFMultiAdmin.ini "${USER_USERNAME} MultiAdminData" Password $(echo -n "${USER_PASSWORD}${USER_USERNAME}" | sha1sum)
crudini --set /home/kf2/.kf2ds/KFGame/server/Config/KFMultiAdmin.ini "${USER_USERNAME} MultiAdminData" Order DenyAllow
crudini --set /home/kf2/.kf2ds/KFGame/server/Config/KFMultiAdmin.ini "${USER_USERNAME} MultiAdminData" bEnabled True

# Set permissions for less privileged user
tee -a /home/kf2/.kf2ds/server/KFGame/Config/KFMultiAdmin.ini << END
Deny=/policy/bans
Deny=/policy/ip
Deny=/settings/general#Server
Deny=/settings/general#Connection
Deny=/settings/general#CheatDetection
Deny=/settings/general#Administration
Deny=/settings/general#MapVoting
Deny=/settings/general#KickVoting
Deny=/settings/general#Chat
Deny=/settings/gametypes
Deny=/settings/maplist
Deny=/settings/serveractors
Deny=/settings/welcome
Deny=/console
Deny=/webadmin
Deny=/multiadmin
END

# Add Magicked bot user to WebAdmin
crudini --set /home/kf2/.kf2ds/server/KFGame/Config/KFMultiAdmin.ini "${BOT_USERNAME} MultiAdminData" DisplayName ${BOT_DISPLAYNAME}
crudini --set /home/kf2/.kf2ds/server/KFGame/Config/KFMultiAdmin.ini "${BOT_USERNAME} MultiAdminData" Password $(echo -n "${BOT_PASSWORD}${BOT_USERNAME}" | sha1sum)
crudini --set /home/kf2/.kf2ds/server/KFGame/Config/KFMultiAdmin.ini "${BOT_USERNAME} MultiAdminData" Order DenyAllow
crudini --set /home/kf2/.kf2ds/server/KFGame/Config/KFMultiAdmin.ini "${BOT_USERNAME} MultiAdminData" bEnabled True

# Sanitise crudini-edited configuration files
printf "Removing extra whitespaces from configuration files...\n"
sed -i 's/ = /=/' /home/kf2/.kf2ds/server/KFGame/Config/LinuxServer-KF*

# Run server instance
printf "Launching server instance\n"
/home/kf2/.kf2ds/server/Binaries/Win64/KFGameSteamServer.bin.x86_64 kf-burningparis?Game=KFGameContent.KFGameInfo_Survival

