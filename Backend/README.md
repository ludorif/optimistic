# optimistic


python -m venv env  
.\env\Scripts\activate     
Flask --app Main run

fastapi dev Main.py --port 5001

//Update requirements from imports 

pipreqs --encoding=utf-8-sig --force   

// Update requirements from local pip 

pip3 freeze > requirements.txt    

docker build --tag optimistic-docker .

Any traffic sent to port 5001 on your host machine will be forwarded to port 5000 within the container.

docker run -d -p 5001:5000 optimistic-docker