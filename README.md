This code is developed and tested in python `3.10.6` It should work with Python version 3.6+

Firstly, let's create a virtual environment:

```zsh
python3 -m venv ~/.venvs/webapp && source ~/.venvs/webapp/bin/activate
```

Installing & upgrading packages:
```zsh
pip install pip -U && pip install -r requirements.txt
```

## 1. Let's create a database
This functionality will scrap web data and save the required fields to a postgresql database.
Simply run this code to scrap the data and create a SQL table in Postgre:
```
python generate_database.py
```

**Data scrapped and saved:** <br />
`id`: ID of job in database (default generation) <br />
`job_id` : Original job id from the website <br />
`job_title`: Title of the job <br />
`seniority_level`: Experience required for the job <br />
`job_location`: Location of the position <br />
`posted_time`: Time elapsed since job posting (1 week ago etc.) (! improvement> today-time elapsed= real date) <br /> 
`job_description`: Full job description <br />
`tech_stack`: It is extracted using tech_stack.txt source and NLTK library. This part can prominently be improved using NLP techniques. <br />

After seeing the logs:
```
DD MM YYYY [INFO]: Table has been successfully created
DD MM YYYY [INFO]: Data has been successfully inserted to table
DD MM YYYY [INFO]: Database has been successfully created
```
we can proceed to next step.

## 2. Running Web App

We can now run the WebApp via:
```
python app.py
```

Please open up your browser go and `http://127.0.0.1:8000/`.
There are 3 endpoints at the moment:
 - `http://127.0.0.1:8000/`: You are going to see a simple json welcoming you
 - `http://127.0.0.1:8000/jobs/`: it will show the table from the database. This data is scrapped, saved to a db and visualized in this route.
 - `http://127.0.0.1:8000/docs/`: This is manual docs from FastAPI. You can see the variables for pagination and sorting.

**Requests are throttled to less than 20 req per min so that site is not affected by
the task

## 3. Unittests

When you are in the root directory of this repository.

Please run:
```
python -m pytest -s -v
```

It will output:

![image](https://user-images.githubusercontent.com/25952802/235351576-84e1c26d-7d3e-49b5-a24b-8a5bf0cf3c9a.png)
