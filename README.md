# Edge-Based Smart Traffic Monitoring System

## Overview

An AI-powered traffic monitoring system that detects, tracks, and counts vehicles from traffic surveillance videos using YOLOv8 and OpenCV. The system processes video locally at the edge, reducing the need to stream raw video data to the cloud.

## Features

* Real-time vehicle detection using YOLOv8
* Multi-object vehicle tracking
* Vehicle counting using a virtual counting line
* Detection of cars, buses, trucks, and motorcycles
* Live visualization of detected vehicles and traffic count

## Technologies Used

* Python
* OpenCV
* YOLOv8 (Ultralytics)
* NumPy

## Current Implementation

### Vehicle Detection

The system uses YOLOv8 to identify vehicles in traffic video streams and draw bounding boxes around detected objects.

### Vehicle Tracking

Each detected vehicle is assigned a unique tracking ID, allowing the system to follow vehicles across multiple frames.

### Vehicle Counting

A virtual counting line is placed on the road. Vehicles are counted when they cross the line, ensuring that each vehicle is counted only once.

## Project Structure

traffic-monitoring/
├── videos/
├── outputs/
├── app.py
├── requirements.txt
└── README.md

## Future Enhancements

* FastAPI Backend
* Database Integration (SQLite/PostgreSQL)
* React Dashboard
* MQTT Communication
* Docker Containerization
* AWS Deployment

## Author

Mukesh Kumar Allari
