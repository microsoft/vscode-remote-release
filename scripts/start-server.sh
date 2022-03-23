#!/usr/bin/env sh
#
# Copyright (c) Microsoft Corporation. All rights reserved.
#

[ "$VSCODE_TRACE" = true ] && set -x

if [ ! "$(command -v curl)" ]; then
    echo "ERROR: Failed to download the VS Code server. 'curl' not installed." 1>&2
    echo "Please install curl:" 1>&2
    echo "Debian/Ubuntu: sudo apt-get install curl" 1>&2
    exit 14
fi

if [ -f /etc/alpine-release ]; then
    case $(uname -m) in
        x86_64)
            INSTALL="server-linux-alpine-web";;
        aarch64)
            INSTALL="server-alpine-arm64-web";;
        *)
            echo "Unknown platform $(uname -m). Falling back to x86_64" 1>&2
            INSTALL="server-linux-alpine-web";;
    esac
    if ! apk info | grep -qxe 'libstdc++'; then
        echo "libstdc++ is required to run the VS Code Server:"  1>&2
        echo "Please open an Alpine shell and run 'apk update && apk add libstdc++'" 1>&2
        exit 12
    fi
elif [ "$(expr \"$OSTYPE\" : \"darwin.*\")" != 0 ]; then
    INSTALL="server-darwin-web"
else
    case $(uname -m) in
        x86_64)
            INSTALL="server-linux-x64-web";;
        aarch64)
            INSTALL="server-linux-arm64-web";;
        *)
            echo "Unknown platform $(uname -m). Falling back to x86_64" 1>&2
            INSTALL="server-linux-x64-web";;
    esac
fi

BUILD_INFO=`curl -s https://update.code.visualstudio.com/api/update/$INSTALL/stable/latest`

DOWNLOAD_URL=$(echo $BUILD_INFO | sed -e 's/.*"url"\:\"\([^\"]*\)\".*/\1/')
NAME=$(echo $BUILD_INFO | sed -e 's/.*"name"\:\"\([^\"]*\)\".*/\1/')
COMMIT=$(echo $BUILD_INFO | sed -e 's/.*"version"\:\"\([^\"]*\)\".*/\1/')

SERVER_DATA_DIR="$HOME/.vscode-server"
SERVER_BUILDS_DIR="$SERVER_DATA_DIR/bin-web"
SERVER_BUILD_DIR="$SERVER_BUILDS_DIR/$COMMIT"

# Check if this version is already installed
if [ ! -d "$SERVER_BUILD_DIR" ]; then

  if [ ! -d "$SERVER_BUILDS_DIR" ]; then
    mkdir -p "$SERVER_BUILDS_DIR"
  else
    # Remove the previous installation attempts
    echo "Removing previous installations...";
    rm -rf "$SERVER_BUILDS_DIR"/????????????????????????????????????????
    rm -rf "$SERVER_BUILDS_DIR"/????????????????????????????????????????-??????????
    rm -rf "$SERVER_BUILDS_DIR"/????????????????????????????????????????-??????????.tar.gz
  fi

  echo Downloading $INSTALL $NAME to $SERVER_BUILD_DIR...

  # Download the .tar.gz file
  SERVER_TAR_FILE="$SERVER_BUILD_DIR-$(date +%s).tar.gz"
  curl -s -o "$SERVER_TAR_FILE" "$DOWNLOAD_URL"
  if [ $? -eq 5 ]; then
    echo "Please install missing certificates." 1>&2
    echo "Debian/Ubuntu:  sudo apt-get install ca-certificates" 1>&2
    exit 13
  fi

  # Unpack the .tar.gz file to a temporary folder name
  SERVER_BUILD_TMP_DIR="$SERVER_BUILD_DIR-$(date +%s)"
  mkdir -p "$SERVER_BUILD_TMP_DIR"
  tar -xf "$SERVER_TAR_FILE" -C "$SERVER_BUILD_TMP_DIR" --strip-components 1

  # Finalize the install
  mv "$SERVER_BUILD_TMP_DIR" "$SERVER_BUILD_DIR"
  rm "$SERVER_TAR_FILE"
fi

$SERVER_BUILD_DIR/bin/code-server "$@"
