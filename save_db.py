import psycopg2
from psycopg2.extras import execute_batch
from get_data import scrapper

TARGET_URL = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Python%20%28Programming%20Language%29&location=Las%20Vegas%2C%20Nevada%2C%20United%20States&geoId=100293800&currentJobId=3415227738&start={}'
TARGET_JOB_URL = 'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'

namedict = scrapper(target_url=TARGET_URL, target_job_url=TARGET_JOB_URL)
print(namedict[0])
# Connect to the database
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="123"
)

# Create a cursor object
cursor = conn.cursor()

query = """INSERT INTO jobs VALUES (default, %(job_id)s, 
        %(job_title)s, 
        %(seniority_level)s, 
        %(job_location)s, 
        %(company_name)s)"""

execute_batch(cursor, query, namedict)

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
