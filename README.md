---
date: 2024-04-17T04:16:36.132054
author: AutoGPT <info@agpt.co>
---

# Jinja API

To create an API that serves HTML print formatted documents like bills, invoices, and receipts utilizing the Jinja package, follow these steps:

1. **Project Setup:**
- Install FastAPI and Uvicorn as the ASGI server to serve your application.
- Install Jinja2 for template rendering and psycopg2 (or asyncpg) for PostgreSQL database interactions.
- Install Prisma as the ORM for database operations.

2. **Database Configuration:**
- Define your models for bills, invoices, and receipts in Prisma schema.
- Perform database migrations to create the necessary tables in PostgreSQL.

3. **API Development:**
- Initialize your FastAPI app.
- Create route handlers for generating bills, invoices, and receipts. Each handler should:
  - Accept necessary data (e.g., customer details, items/services, amounts, etc.) through request payloads.
  - Query the database for any needed additional information.
  - Use Jinja templates for generating the document in HTML format. Implement the designs and layouts as specified or allow for template customization.

4. **Jinja Template Rendering:**
- Store your Jinja templates in a designated folder within your project.
- In each route handler, use Jinja's `Environment` and `FileSystemLoader` to load the template.
- Render the template with the provided data to produce the HTML document.

5. **Serving Document:**
- Serve the rendered HTML directly to the client or offer an option to download it as a PDF. You might need additional libraries like WeasyPrint for PDF generation.

6. **Testing and Deployment:**
- Test your API endpoints with various data inputs to ensure the documents are generated correctly and layouts are as desired.
- Deploy your FastAPI application using Uvicorn, and consider using Docker for easier deployment and scalability.

**Key Points from Task Discussion:**
- The user prefers clear, minimalist designs for all documents, with easily readable details and customizable templates for branding.
- Best practices for Jinja templates include using semantic HTML/CSS, template inheritance, page break control, data optimization, and accessibility considerations.

This setup combines Python, FastAPI, PostgreSQL, and Prisma, leveraging Jinja for dynamic HTML document rendering based on user requirements and design preferences.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'Jinja API'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
