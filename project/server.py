import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List

import project.generate_bill_service
import project.generate_invoice_service
import project.generate_receipt_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="Jinja API",
    lifespan=lifespan,
    description="To create an API that serves HTML print formatted documents like bills, invoices, and receipts utilizing the Jinja package, follow these steps:\n\n1. **Project Setup:**\n- Install FastAPI and Uvicorn as the ASGI server to serve your application.\n- Install Jinja2 for template rendering and psycopg2 (or asyncpg) for PostgreSQL database interactions.\n- Install Prisma as the ORM for database operations.\n\n2. **Database Configuration:**\n- Define your models for bills, invoices, and receipts in Prisma schema.\n- Perform database migrations to create the necessary tables in PostgreSQL.\n\n3. **API Development:**\n- Initialize your FastAPI app.\n- Create route handlers for generating bills, invoices, and receipts. Each handler should:\n  - Accept necessary data (e.g., customer details, items/services, amounts, etc.) through request payloads.\n  - Query the database for any needed additional information.\n  - Use Jinja templates for generating the document in HTML format. Implement the designs and layouts as specified or allow for template customization.\n\n4. **Jinja Template Rendering:**\n- Store your Jinja templates in a designated folder within your project.\n- In each route handler, use Jinja's `Environment` and `FileSystemLoader` to load the template.\n- Render the template with the provided data to produce the HTML document.\n\n5. **Serving Document:**\n- Serve the rendered HTML directly to the client or offer an option to download it as a PDF. You might need additional libraries like WeasyPrint for PDF generation.\n\n6. **Testing and Deployment:**\n- Test your API endpoints with various data inputs to ensure the documents are generated correctly and layouts are as desired.\n- Deploy your FastAPI application using Uvicorn, and consider using Docker for easier deployment and scalability.\n\n**Key Points from Task Discussion:**\n- The user prefers clear, minimalist designs for all documents, with easily readable details and customizable templates for branding.\n- Best practices for Jinja templates include using semantic HTML/CSS, template inheritance, page break control, data optimization, and accessibility considerations.\n\nThis setup combines Python, FastAPI, PostgreSQL, and Prisma, leveraging Jinja for dynamic HTML document rendering based on user requirements and design preferences.",
)


@app.post(
    "/generate/invoice",
    response_model=project.generate_invoice_service.GenerateInvoiceResponse,
)
async def api_post_generate_invoice(
    customer_name: str,
    customer_address: str,
    invoice_number: str,
    date_issued: str,
    due_date: str,
    items: List[project.generate_invoice_service.InvoiceItem],
    subtotal: float,
    tax_rate: float,
    total_amount: float,
    template_id: str,
) -> project.generate_invoice_service.GenerateInvoiceResponse | Response:
    """
    Generates an invoice document based on provided data.
    """
    try:
        res = await project.generate_invoice_service.generate_invoice(
            customer_name,
            customer_address,
            invoice_number,
            date_issued,
            due_date,
            items,
            subtotal,
            tax_rate,
            total_amount,
            template_id,
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/generate/bill", response_model=project.generate_bill_service.GenerateBillResponse
)
async def api_post_generate_bill(
    client_name: str,
    client_address: str,
    billing_date: str,
    due_date: str,
    bill_items: List[project.generate_bill_service.BillItem],
) -> project.generate_bill_service.GenerateBillResponse | Response:
    """
    Generates a bill document based on provided data.
    """
    try:
        res = await project.generate_bill_service.generate_bill(
            client_name, client_address, billing_date, due_date, bill_items
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/generate/receipt",
    response_model=project.generate_receipt_service.GenerateReceiptResponse,
)
async def api_post_generate_receipt(
    customer_name: str,
    customer_email: str,
    items: List[project.generate_receipt_service.Item],
    total_amount: float,
    receipt_date: datetime,
    pdf_requested: bool,
) -> project.generate_receipt_service.GenerateReceiptResponse | Response:
    """
    Generates a receipt document based on provided data.
    """
    try:
        res = await project.generate_receipt_service.generate_receipt(
            customer_name,
            customer_email,
            items,
            total_amount,
            receipt_date,
            pdf_requested,
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
