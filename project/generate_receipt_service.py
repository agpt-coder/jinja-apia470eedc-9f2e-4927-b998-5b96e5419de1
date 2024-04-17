from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel


class Item(BaseModel):
    """
    This type represents a single item in a purchase
    """

    name: str
    quantity: int
    price: float


class GenerateReceiptResponse(BaseModel):
    """
    This model represents the output of the receipt generation process, including a link or the actual generated receipt document.
    """

    receipt_id: str
    receipt_link: Optional[str] = None
    receipt_html: Optional[str] = None


async def generate_receipt(
    customer_name: str,
    customer_email: str,
    items: List[Item],
    total_amount: float,
    receipt_date: datetime,
    pdf_requested: bool,
) -> GenerateReceiptResponse:
    """
    Generates a receipt document based on provided data.

    Args:
    customer_name (str): Name of the customer for whom the receipt is generated.
    customer_email (str): Email address of the customer.
    items (List[Item]): A list of items that were purchased.
    total_amount (float): Total amount for the receipt.
    receipt_date (datetime): The date the receipt is issued.
    pdf_requested (bool): Flag to request the receipt in PDF format. Defaults to false, returning an HTML response instead.

    Returns:
    GenerateReceiptResponse: This model represents the output of the receipt generation process, including a link or the actual generated receipt document.
    """
    receipt_id = str(uuid4())
    data = {
        "customer_name": customer_name,
        "customer_email": customer_email,
        "items": items,
        "total_amount": total_amount,
        "receipt_date": receipt_date.strftime("%Y-%m-%d"),
    }
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("receipt_template.html")
    rendered_html = template.render(data)
    if pdf_requested:
        pdf_path = f"receipts/{receipt_id}.pdf"
        receipt_link = f"http://yourserver.com/{pdf_path}"
        return GenerateReceiptResponse(receipt_id=receipt_id, receipt_link=receipt_link)
    else:
        return GenerateReceiptResponse(
            receipt_id=receipt_id, receipt_html=rendered_html
        )
