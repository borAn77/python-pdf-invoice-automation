from PyPDF2 import PdfReader
import re
import pandas as pd
import os

input_pdf = "sample.pdf"
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

reader = PdfReader(input_pdf)

text = ""
for page in reader.pages:
    page_text = page.extract_text()
    if page_text:
        text += page_text + "\n"

# --- Simple invoice field extraction ---
invoice_number = re.search(r"Invoice Number:\s*(.*)", text)
date = re.search(r"Date:\s*(.*)", text)
total = re.search(r"Total:\s*([0-9]+)\s*PLN", text)

data = {
    "Invoice Number": invoice_number.group(1) if invoice_number else "",
    "Date": date.group(1) if date else "",
    "Total (PLN)": total.group(1) if total else "",
}

df = pd.DataFrame([data])

output_csv = os.path.join(output_dir, "invoice_data.csv")
df.to_csv(output_csv, index=False)

print("Invoice data extracted:")
print(df)
print(f"Saved to {output_csv}")
