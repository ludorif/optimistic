# 🌱 Optimistic

**Optimistic** is an open-source project designed with several goals in mind:

- Showcase my full-stack and AI development skills
- Experiment with and test emerging technologies
- Build a playful space that envisions an optimistic, climate-positive world

---

## 🛠 Tech Stack

- **Backend:** Python with FastAPI
- **Frontend:** React (JavaScript)
- **AI:** Gemini API to generate events from user stories
- **Media:** Pexels API for imagery
- **Database:** MongoDB
- **Hosting:** Render.com

---

## ✨ Concept

The platform works around the idea of daily optimistic events:

- Users can submit events
- The community votes for their favorite event of the day
- A winner is declared daily

All events are intentionally uplifting, imaginative, and climate-positive, ensuring a positive and future-focused experience.

---



## 🗺 Roadmap

- Deepen AI integrations and experimentation
- Introduce multiple worlds for diverse optimistic scenarios
- Enhance the UI/UX design for a more engaging look and feel

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