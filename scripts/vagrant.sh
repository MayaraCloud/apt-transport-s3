#!/bin/bash

sudo apt-get update

packages=(libapt-pkg-dev libcurl4-openssl-dev dpkg-dev debhelper cdbs)

for p in "${packages[@]}"
do
  apt-get install -y --force-yes "${p}"
done

