# optimistic
#  Copyright (c) 2025 Ludovic Riffiod

python -m venv env  
.\env\Scripts\activate     
Flask --app Main run

fastapi dev Main.py --port 5001

//Update requirements from imports 

pipreqs --encoding=utf-8-sig --force   

// Update requirements from local pip 

pip3 freeze > requirements.txt    

docker build -t optimistic-docker -f Backend/Dockerfile .

Any traffic sent to port 5001 on your host machine will be forwarded to port 5000 within the container.

docker run -d -p 5001:5001 optimistic-docker

$env:MONGO_DB_URI=
$env:GEMINI_API_KEY =
$env:PEXELS_API_KEY=