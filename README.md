# Survey Application

##  Setup & Run Locally

###  Backend (REST API)

1. **Clone the backend repository**
   ```bash
   git clone https://github.com/oderojohn/sky_survey_backend.git
   cd survey-api
   ```

2. **Create and activate a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations and start the server**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

   The backend should now be running at [http://localhost:8000](http://localhost:8000)

---



### Backend ( Render)
1. Push your backend code to GitHub.
2. Connect your GitHub repo to a deployment platform ( Render).
3. Set necessary environment variables (e.g. `SECRET_KEY`, `DEBUG`, DB settings).
4. Run initial migration and start server.


##  Postman Collection JSON

```json
{
  "info": {
    "name": "Survey API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
    "description": "Collection for testing survey API endpoints"
  },
  "item": [
    {
      "name": "Get Questions",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:8000/api/questions/",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "questions"]
        }
      }
    },
    {
      "name": "Submit Response (with Certificates)",
      "request": {
        "method": "POST",
        "header": [],
        "body": {
          "mode": "formdata",
          "formdata": [
            { "key": "full_name", "value": "John Doe", "type": "text" },
            { "key": "email_address", "value": "john@example.com", "type": "text" },
            { "key": "description", "value": "This is my survey response.", "type": "text" },
            { "key": "gender", "value": "male", "type": "text" },
            { "key": "programming_stack", "value": "Python, React", "type": "text" },
            { "key": "certificates", "type": "file", "src": ["path/to/certificate1.pdf"] },
            { "key": "certificates", "type": "file", "src": ["path/to/certificate2.pdf"] }
          ]
        },
        "url": {
          "raw": "http://localhost:8000/api/responses/",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "responses"]
        }
      }
    },
    {
      "name": "Get Responses by Email",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:8000/api/responses/?email_address=john@example.com",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "responses"],
          "query": [
            { "key": "email_address", "value": "john@example.com" }
          ]
        }
      }
    },
    {
      "name": "Download Certificate by ID",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:8000/api/certificates/1/download/",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "certificates", "1", "download"]
        }
      }
    },
    {
      "name": "Download All Certificates (Batch)",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:8000/api/certificates/batch-download/?response_id=1",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "certificates", "batch-download"],
          "query": [
            { "key": "response_id", "value": "1" }
          ]
        }
      }
    }
  ]
}
```

