"""Main script for Web App"""
from typing import List
import uvicorn
from fastapi import FastAPI, HTTPException, Query, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import psycopg2
from psycopg2.extras import RealDictCursor

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

conn_params = {
    "host":"localhost",
    "database":"postgres",
    "user":"postgres",
    "password":"123"
    }

@app.get("/")
async def startup():
    """function on start"""
    return {"Hello":"Beekin!!!"}

@app.get("/jobs/")
@limiter.limit("20/minute") ## Throttle requests to less than 20 req per min so that site is not affected by the task
async def get_jobs(
        request: Request,
        page: int = Query(1, ge=1, description="Page number, starting from 1"),
        per_page: int = Query(10, ge=1, le=100, description="Number of jobs per page"),
        sort_by: str = Query("company_name", description="Field to sort by"),
        sort_order: str = Query("desc", description="Sort order (asc or desc)")
    ) -> List[dict]:
    """actual functions to fetch data from database"""
    offset = (page - 1) * per_page

    # Define the SQL query to fetch job data with pagination and sorting
    sql_query = f"""
        SELECT DISTINCT *
        FROM jobs
        WHERE job_location IS NOT NULL
        ORDER BY {sort_by} {sort_order}
        LIMIT %(per_page)s
        OFFSET %(offset)s;
    """

    # Create a connection to the PostgreSQL database
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                sql_query,
                {
                    "per_page": per_page,
                    "offset": offset,
                },
            )
            job_data = cur.fetchall()

    if not job_data:
        raise HTTPException(status_code=404, detail="No jobs found")

    return job_data

if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)
