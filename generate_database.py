"""Script is being used for generating a database for WebApp"""
import logging
import psycopg2
from psycopg2.extras import execute_batch
from utils.get_data import scrapper

# Define constants
TARGET_URL = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Python%20%28Programming%20Language%29&location=Las%20Vegas%2C%20Nevada%2C%20United%20States&geoId=100293800&currentJobId=3415227738&start={}'
TARGET_JOB_URL = 'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'
DB_CONFIG = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': '123'
}

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    handlers=[
        logging.FileHandler('database.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Scrape job data from LinkedIn
namedict = scrapper(target_url=TARGET_URL, target_job_url=TARGET_JOB_URL)

try:
    # Connect to the database
    with psycopg2.connect(**DB_CONFIG) as conn:
        # Create a cursor object
        with conn.cursor() as cursor:
            # Create the jobs table
            CREATE_TABLE = """
                DROP TABLE IF EXISTS jobs;
                CREATE TABLE jobs (
                    id SERIAL PRIMARY KEY,
                    job_id VARCHAR(255), 
                    job_title VARCHAR(255), 
                    seniority_level VARCHAR(255),
                    job_location VARCHAR(255),
                    company_name VARCHAR(255),
                    tech_stack VARCHAR(255),
                    job_description TEXT
                );
            """
            cursor.execute(CREATE_TABLE)
            logger.info('Table has been successfully created')

            # Insert the job data into the jobs table
            INSERT_DATA = """
                INSERT INTO jobs (job_id, job_title, seniority_level, job_location, company_name, tech_stack, job_description)
                VALUES (%(job_id)s, %(job_title)s, %(seniority_level)s, %(job_location)s, %(company_name)s, %(tech_stack)s, %(job_description)s)
            """
            execute_batch(cursor, INSERT_DATA, namedict)
            logger.info('Data has been successfully inserted to table')

    logger.info('Database has been successfully created')

except psycopg2.Error as e:
    logger.error('Error connecting to the database: %s', e)
