# 🌱 Optimistic

## Env variables 
- $env:MONGO_DB_URI=
- $env:GEMINI_API_KEY =
- $env:PEXELS_API_KEY=

## Commands
- (local) fastapi dev backend/Main.py --port 5001
- docker build -t optimistic-docker -f Backend/Dockerfile .
- docker run -d -p 5001:5001 optimistic-docker

- //Update requirements from imports 
- pipreqs --encoding=utf-8-sig --force   
- // Update requirements from local pip 
- pip3 freeze > requirements.txt    


# Copyright (c) 2025 Ludovic Riffiod