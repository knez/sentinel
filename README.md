# Project Sentinel

A simple open-source camera surveillance system in Python3

<img src="https://i.imgur.com/08G6kz9.png" width="250">


## Overview

This project implements a simple indoor home security solution using OpenCV library. The app can detect *intruders* and upload short video footages to the main web dashboard, where users can replay and manage the videos. Optionally, a user has the ability to get notified via email.

The project is split into two entirely **separate** modules called `camera` and `web-dashboard`. Each of those modules are designed to run independently of each other. 

## Camera module 

This module represents the main detection engine responsible for detecting motion, categorising intruders and locating their position on the screen. It also includes video capturing and uploading capabilities. 

### Installation

Create a new environment `venv-camera` and activate it

```bash
$ cd camera
$ python -m venv venv-camera
$ .\venv-camera\Scripts\Activate.ps1
# alternatively ./venv-camera/bin/activate on Linux
```

Install all required dependencies

```bash
$ pip install -r requirements.txt
```

Optionally, configure the `settings.yaml` file to your liking

Run the module

```bash
$ python detect.py
```

or alternatively 

```
python detect.py --debug
```

if you want to see the camera window and more verbose logging

## Web-dashboard module

Web dashboard is a single-user webapp where user can manage video footages, see associated metadata, and replay/delete videos. It also allows one to enable/disable the additional email notification alert.

### Installation 

In a separate terminal window, create a new environment and activate it

```bash
$ cd web-dashboard
$ python -m venv venv-dashboard
$ .\venv-dashboard\Scripts\Activate.ps1
```

Install all required dependencies

```bash
$ pip install -r requirements.txt
```

Run the dashboard

```bash
$ python run_webserver.py
```

The dashboard can then be accessed at http://localhost:8080, using the default login credentials `admin:admin`

