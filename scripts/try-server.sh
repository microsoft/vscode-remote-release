#!/usr/bin/env sh
#
# Copyright (c) Microsoft Corporation. All rights reserved.
#

[ "$VSCODE_TRACE" = true ] && set -x

if [ ! "$(command -v wget)" ]; then
	echo "ERROR: Failed to download the VS Code server. 'wget' not installed." 1>&2
	echo "Please install wget:" 1>&2
	echo "Debian/Ubuntu: sudo apt-get install wget" 1>&2
	exit 14
fi

if [ -f /etc/alpine-release ]; then
	case $(uname -m) in
		x86_64)
			INSTALL="server-linux-x64-alpine";;
		aarch64)
			INSTALL="server-alpine-arm64-web";;
		*)
			echo "Unknown platform $(uname -m). Falling back to x86_64" 1>&2
			INSTALL="server-linux-x64-alpine";;
	esac
	if ! apk info | grep -qxe 'libstdc++'; then
		echo "libstdc++ is required to run the VS Code Server:"  1>&2
		echo "Please open an Alpine shell and run 'apk update && apk add libstdc++'" 1>&2
		exit 12
	fi
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

BUILD_INFO=`curl -s -X GET https://update.code.visualstudio.com/api/update/$INSTALL/insider/latest`

DOWNLOAD_URL=$(echo $BUILD_INFO | sed -e 's/.*"url"\:\"\([^\"]\+\)\".*/\1/m')
NAME=$(echo $BUILD_INFO | sed -e 's/.*"name"\:\"\([^\"]\+\)\".*/\1/m')
COMMIT=$(echo $BUILD_INFO | sed -e 's/.*"version"\:\"\([^\"]\+\)\".*/\1/m')

SERVER_DATA_DIR="$HOME/.vscode-server-insiders"
SERVER_BUILDS_DIR="$SERVER_DATA_DIR/bin-web"
SERVER_BUILD_DIR="$SERVER_BUILDS_DIR/$COMMIT"

# Check if this version is already installed
if [ ! -d "$SERVER_BUILD_DIR" ]; then

  if [ ! -d "$SERVER_BUILDS_DIR" ]; then
    mkdir -p "$SERVER_BUILDS_DIR"
  else
    # Remove the previous installation attempts
    rm -rf "$SERVER_BUILDS_DIR"/????????????????????????????????????????-??????????
    rm -rf "$SERVER_BUILDS_DIR"/????????????????????????????????????????-??????????.tar.gz
  fi

  echo Downloading $INSTALL $NAME to $SERVER_BUILD_DIR...

  # Download the .tar.gz file
  SERVER_TAR_FILE="$SERVER_BUILD_DIR-$(date +%s).tar.gz"
  wget -O "$SERVER_TAR_FILE" "$DOWNLOAD_URL"
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

CONNECTION_TOKEN_FILE="$SERVER_DATA_DIR/.server_connection_token";

if [ ! -f "$CONNECTION_TOKEN_FILE" ]; then
  CONNECTION_TOKEN=$(expr $$ "*" $(date +%s))
  echo $CONNECTION_TOKEN > $CONNECTION_TOKEN_FILE
else
  CONNECTION_TOKEN=$(cat $CONNECTION_TOKEN_FILE)
fi

$SERVER_BUILD_DIR/bin/code-server-insiders --connection-token-file=$CONNECTION_TOKEN_FILE --port=7777 --host=localhost
