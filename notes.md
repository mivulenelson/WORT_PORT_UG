A SIMPLE DIGITAL BUS TICKET BOOKING SYSTEM IN UGANDA BY MIVULE NELSON

-->It uses a custom user management model to authenticate users

-->A user can then book a bus ticket based on the available buses

-->If a bus is past its time of departure, its archived and the user can not book a ticket for that bus

-->I have not included payments in this system, as can be included at any time of need in the future

-->I have used the python uvicorn as an ASGI server, celery to schedule tasks of sending emails to users and docker to containerize Django, Celery, RabbitMQ, Redis and Flower

-->It implements Django channels for Websocket communication

-->It sends reminders to users if they book for any ticket, 30 minutes after booking and 30 minutes before departure


FOLLOW THE STEPS BELOW TO RUN THE PROJECT

1. Download the full folder of the project into your computer from my git account 
()
2. python3 -m venv env_name, to install a virtual environment
3. source env_name/bin/activate, to activate the environment
4. pip install django==5.0
5. pip install pillow, for images
6. pip install channels
7. pip install celery flower django-celery-beat
8. pip install channels-redis
9. pip install uvicorn, as ASGI server
10. Go to docker website and install docker on your system based on your os, but make sure even docker-desktop is installed
11. Run, docker-compose up -d --build, to start the project at port: 8000
12. Type, 127.0.0.1:8000, in your browser to open the project