#
# Copyright (c) Microsoft Corporation. All rights reserved.
#
$OldProgressPreference = $ProgressPreference
$ProgressPreference = 'SilentlyContinue' # turn off progress reporting as it slows down Invoke-WebRequest

$Install = "server-win32-x64-web"

$Url = "https://update.code.visualstudio.com/api/update/$Install/stable/latest"
$BuildInfo = (Invoke-WebRequest -Uri $Url -UseBasicParsing).Content | ConvertFrom-Json

$DownloadURL=$BuildInfo.url
$Name=$BuildInfo.name
$Commit=$BuildInfo.version

$ServerDataDir="$home\.vscode-server"
$ServerBuildsDir="$ServerDataDir\bin-web"
$ServerBuildDir="$ServerBuildsDir\$Commit"

if (!(Test-Path -Path "$ServerBuildDir")){
	if (!(Test-Path -Path "$ServerBuildsDir")){
		[void](New-Item -Type Directory -Path "$ServerBuildsDir")
	} else {
		Write-Host "Removing previous installations..."
		Remove-Item -Recurse -Force -Path "$ServerBuildsDir\????????????????????????????????????????"
		Remove-Item -Recurse -Force -Path "$ServerBuildsDir\????????????????????????????????????????-??????????"
		Remove-Item -Path "$ServerBuildsDir\????????????????????????????????????????-??????????.zip"
	}

	$DownloadTimestamp = [int] (Get-Date -UFormat %s)

	# Download the build
	Write-Host Downloading $Install $Name to $ServerBuildDir...
	$ServerZipFile = "$ServerBuildDir-$DownloadTimestamp.zip"
	Invoke-WebRequest -Uri $DownloadURL -OutFile $ServerZipFile

	# Unpack the .zip file to a temporary folder name
	Write-Host Extracting files...

	$ServerBuildTempDir = "$ServerBuildDir-$DownloadTimestamp"
	Add-Type -Assembly "System.IO.Compression.Filesystem" # Faster than using Expand-Archive
	[System.IO.Compression.ZipFile]::ExtractToDirectory("$ServerZipFile", "$ServerBuildTempDir")
 
	# Finalize the install
	Move-Item -Path "$ServerBuildTempDir\vscode-$Install" -Destination "$ServerBuildDir"
	Remove-Item -Path "$ServerBuildTempDir"
	Remove-Item -Path "$ServerZipFile"
}

$ProgressPreference = $OldProgressPreference

Invoke-Expression -Command "$ServerBuildDir\bin\code-server.cmd $args" 
