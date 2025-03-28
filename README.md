# Integrity Checker


A command-line tool that detects potentially hidden interview coding processes and applications that might be running in the background during screen sharing sessions.


## Features


- Detects running processes related to interview coding platforms
- Checks if these processes have visible windows
- Scans for suspicious applications in system directories
- Provides colored status output (green for safe, red for suspicious)
- Works on both Windows and macOS
- Available as a standalone binary or Python script


## Installation


### Option 1: Using the Binary (Recommended)


1. Download the appropriate binary for your system:
- For macOS: `integritychecker-mac`
- For Windows: `integritychecker-windows.exe`
2. Make the binary executable (macOS/Linux only):
  ```bash
  chmod +x integritychecker-mac
  ```


### Option 2: From Source


1. Clone this repository or download the files
2. Install the required dependencies:
  ```bash
  pip install -r requirements.txt
  ```


## Usage


### Using the Binary


On macOS/Linux:
```bash
./integritychecker-mac
```


On Windows:
```bash
integritychecker-windows.exe
```


### Using the Python Script


```bash
python integritychecker.py
```


### Output


- Green status (✅): No suspicious processes or applications detected
- Red status (⚠️): Potentially hidden interview coding processes or applications detected


## Building the Binary


To build the binary from source:


1. Install the requirements:
  ```bash
  pip install -r requirements.txt
  ```


2. Build the binary:
  ```bash
  pyinstaller integritychecker.spec
  ```


The binary will be created in the `dist` directory.


## How it Works


The tool:
1. Scans for running processes
2. Identifies processes related to interview coding platforms
3. Checks if these processes have visible windows
4. Scans system directories for suspicious applications
5. Reports suspicious processes and applications


## Requirements


### For Running the Binary
- Windows or macOS operating system
- No additional requirements


### For Running from Source
- Python 3.6 or higher
- Windows or macOS operating system
- Required Python packages (listed in requirements.txt)


## Note


This tool is designed to help maintain integrity during remote interviews by detecting potentially hidden coding assistance tools. It's recommended to run this tool before starting any screen sharing session.
