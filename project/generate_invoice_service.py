import json
from typing import List, Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class InvoiceItem(BaseModel):
    """
    Details of each item or service included in the invoice.
    """

    description: str
    quantity: int
    unit_price: float
    total_price: float


class GenerateInvoiceResponse(BaseModel):
    """
    The response model for the invoice generation request indicating the result and providing access to the generated document.
    """

    success: bool
    message: str
    document_url: Optional[str] = None


async def generate_invoice(
    customer_name: str,
    customer_address: str,
    invoice_number: str,
    date_issued: str,
    due_date: str,
    items: List[InvoiceItem],
    subtotal: float,
    tax_rate: float,
    total_amount: float,
    template_id: str,
) -> GenerateInvoiceResponse:
    """
    Generates an invoice document based on provided data.

    Args:
        customer_name (str): The name of the customer being invoiced.
        customer_address (str): The address of the customer.
        invoice_number (str): The unique invoice number for tracking.
        date_issued (str): The date when the invoice was issued.
        due_date (str): The due date for the invoice payment.
        items (List[InvoiceItem]): A list of items or services billed with their details.
        subtotal (float): The subtotal amount before taxes.
        tax_rate (float): The applicable tax rate for the invoice.
        total_amount (float): The final total amount including taxes.
        template_id (str): Optional ID for a custom invoice template from the Template model.

    Returns:
        GenerateInvoiceResponse: The response model for the invoice generation request indicating the result and providing access to the generated document.
    """
    try:
        template = await prisma.models.Template.prisma().find_unique(
            where={"id": template_id}
        )
        if not template:
            return GenerateInvoiceResponse(success=False, message="Template not found")
        invoice_data = {
            "customer_name": customer_name,
            "customer_address": customer_address,
            "invoice_number": invoice_number,
            "date_issued": date_issued,
            "due_date": due_date,
            "items": [item.dict() for item in items],
            "subtotal": subtotal,
            "tax_rate": tax_rate,
            "total_amount": total_amount,
        }
        rendered_document = template.html
        document = await prisma.models.Document.prisma().create(
            data={
                "title": f"Invoice {invoice_number}",
                "content": json.dumps(
                    {"renderedDocument": rendered_document, "data": invoice_data}
                ),
                "type": prisma.enums.DocumentType.INVOICE,
                "ownerId": "owner-id-placeholder",
            }
        )
        document_url = f"http://example.com/documents/{document.id}"
        return GenerateInvoiceResponse(
            success=True,
            message="Invoice generated successfully",
            document_url=document_url,
        )
    except Exception as e:
        return GenerateInvoiceResponse(success=False, message=str(e))
