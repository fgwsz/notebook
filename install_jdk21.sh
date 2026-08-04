#!/bin/bash

sudo apt update
sudo apt install openjdk-21-jdk -y
java -version
javac -version
echo "export JAVA_HOME='/usr/lib/jvm/java-21-openjdk-amd64'" >> ~/.bashrc
