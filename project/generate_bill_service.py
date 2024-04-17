from typing import List, Optional

import prisma
import prisma.enums
import prisma.models
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import BaseModel


class BillItem(BaseModel):
    """
    Represents an individual item or service charged on the bill.
    """

    description: str
    quantity: int
    unit_price: float
    total: float


class GenerateBillResponse(BaseModel):
    """
    Output model for bill document generation containing status and access URLs.
    """

    status: str
    document_url: str
    pdf_conversion_url: Optional[str] = None


async def generate_bill(
    client_name: str,
    client_address: str,
    billing_date: str,
    due_date: str,
    bill_items: List[BillItem],
) -> GenerateBillResponse:
    """
    Generates a bill document based on provided data.

    Args:
        client_name (str): Name of the client billed.
        client_address (str): Address of the client.
        billing_date (str): Date when the bill is issued.
        due_date (str): Due date for the bill payment.
        bill_items (List[BillItem]): List of items or services billed.

    Returns:
        GenerateBillResponse: Output model for bill document generation containing status and access URLs.
    """
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("bill_template.html")
    context = {
        "client_name": client_name,
        "client_address": client_address,
        "billing_date": billing_date,
        "due_date": due_date,
        "bill_items": bill_items,
    }
    rendered_document = template.render(context)
    document = await prisma.models.Document.prisma().create(
        data={
            "title": f"Bill for {client_name}",
            "content": {"renderedDocument": rendered_document},
            "type": prisma.enums.DocumentType.BILL,
            "ownerId": "user_id_here",
        }
    )
    document_url = f"http://example.com/documents/{document.id}"
    pdf_conversion_url = f"http://example.com/documents/{document.id}/convert"
    return GenerateBillResponse(
        status="generated",
        document_url=document_url,
        pdf_conversion_url=pdf_conversion_url,
    )
