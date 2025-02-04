 #facebookinsight
README.md
# Facebook Insights Microservice

A microservice for fetching and storing Facebook page insights using FastAPI and MongoDB.

## Setup

1. **Clone the repository**:
   ```
   bash
   git clone https://github.com/yourusername/facebook_insights.git
   cd facebook_insights
   ```
Install dependencies:  
  
pip install -r requirements.txt  
Create a .env file with MongoDB URI and database name:  
  
MONGO_URI=mongodb://yourUsername:yourPassword@localhost:27017/  
DATABASE_NAME=facebook_insights  
Run the application:  
  
uvicorn app.main:app --reload 

Usage  

Get Page Details  
GET /pages/{username}:  
curl -X 'GET' 'http://127.0.0.1:8000/pages/boat.lifestyle' -H 'accept: application/json'  

Search Pages  

GET /pages/:  
curl -X 'GET' 'http://127.0.0.1:8000/pages/?min_followers=20000&max_followers=40000&name=boat' -H 'accept: application/json'  

Get Recent Posts  

GET /posts/{username}:  
curl -X 'GET' 'http://127.0.0.1:8000/posts/boat.lifestyle?limit=10' -H 'accept: application/json' 

Get Followers  

GET /followers/{username}:  
curl -X 'GET' 'http://127.0.0.1:8000/followers/boat.lifestyle?page=1&limit=20' -H 'accept: application/json'  
