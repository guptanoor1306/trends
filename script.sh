#!/bin/bash

# Install necessary dependencies
apt-get update
apt-get install -y wget unzip google-chrome-stable #Ensure Chrome is installed

# Create a directory for ChromeDriver
mkdir -p /usr/local/share/chromedriver
cd /usr/local/share/chromedriver

# Get the latest stable Chrome version
CHROME_VERSION=$(google-chrome --version | cut -d' ' -f3 | cut -d'.' -f1)

# Get the latest ChromeDriver version that supports Chrome $CHROME_VERSION
CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")

# Debugging: Print the ChromeDriver version
echo "ChromeDriver Version: $CHROMEDRIVER_VERSION"

# Download ChromeDriver
wget "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"

# Unzip ChromeDriver
unzip chromedriver_linux64.zip

# Make ChromeDriver executable
chmod +x chromedriver

# Add /usr/local/share/chromedriver to PATH (more specific than /usr/local/bin)
export PATH=$PATH:/usr/local/share/chromedriver

# Debugging: Print the current PATH
echo "Current PATH: $PATH"

#Debugging test run
chromedriver --version

echo "ChromeDriver installed and PATH updated successfully!"
