# dailyReturnApi


## Project description

####  Main purpose
API Service for sending the daily return amount of a stock portfolio.



#### Problem i wanted to solve
The idea for this project came from 2 issues. 
1. I wanted to learn Docker 
2. My main portfolio website needed a small service to get the daily return for a specific stock portfolio

##### Issue 1. Learn Docker

I can't count how many times I read about Docker or the amount of example applications used with Docker. After reading about how much times it saves and confient it must be, it was time to learn Docker. 

##### Issue 2. Main issue: Get the daily return from my stock portfolio used in my Stocktracker app

I was looking for a nice project to learn building a RESTful api and docker. After refactoring the interface of my stocktracker app I added a new KPI named 'Daily return'. This figure shows whenever the user opens his portfolio detail page, the daily return in regard to yesterday. 

####  Technology stack
<p align="left">
   <a href="https://fastapi.tiangolo.com/" target="_blank" rel="noreferrer"> <img
      src="https://github.com/devicons/devicon/blob/master/icons/fastapi/fastapi-original-wordmark.svg"
      alt="fastapi" width="40" height="40"/> </a>
   <a href="https://www.postgresql.org" target="_blank" rel="noreferrer"> <img
      src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original-wordmark.svg"
      alt="postgresql" width="40" height="40"/> </a>
   <a href="https://www.docker.com/" target="_blank" rel="noreferrer"> <img
      src="https://github.com/devicons/devicon/blob/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40"
      height="40"/> </a>
</p>

My goal was to build a RESTful Api which implemented the basic CRUD (CREATE, READ, UPDATE, DELETE) operations following the restfull architectural style. 
####  Challenges and future improvements

### How to run
`gunicorn -k uvicorn.workers.UvicornWorker main:app -b :8000`
