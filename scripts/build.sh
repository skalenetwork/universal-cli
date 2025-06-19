#!/usr/bin/env bash

set -e

VERSION=$1
BRANCH=$2

USAGE_MSG='Usage: build.sh [VERSION] [BRANCH]'

if [ -z "$1" ]
then
    (>&2 echo 'You should provide version')
    echo $USAGE_MSG
    exit 1
fi

if [ -z "$2" ]
then
    (>&2 echo 'You should provide git branch')
    echo $USAGE_MSG
    exit 1
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PARENT_DIR="$(dirname "$DIR")"

OS=`uname -s`-`uname -m`
EXECUTABLE_NAME=uni-$VERSION-$OS

pyinstaller main.spec

mv $PARENT_DIR/dist/main $PARENT_DIR/dist/$EXECUTABLE_NAME

echo "========================================================================================="
echo "Built node-cli v$VERSION, branch: $BRANCH"
echo "Executable: $EXECUTABLE_NAME"
