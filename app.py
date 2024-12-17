from flask import Flask, request, send_file
import qrcode
from io import BytesIO
from fpdf import FPDF

app = Flask(__name__)

@app.route('/generate_qr', methods=['GET'])
def generate_qr():
    subject = request.args.get('subject', 'No Subject')
    content = request.args.get('content', 'Default Content')
    qr_data = request.args.get('qr_data', 'https://example.com')

    # Generate QR code in memory
    qr = qrcode.make(qr_data)
    qr_buffer = BytesIO()
    qr.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)

    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt=subject, ln=True, align="C")

    # Use BytesIO object for QR code image
    qr_buffer.seek(0)
    pdf.image(qr_buffer, x=80, y=50, w=50, h=50, type='PNG')

    # Add content text
    pdf.set_font("Arial", size=12)
    pdf.ln(70)
    pdf.multi_cell(0, 10, txt=content)

    # Output PDF to memory
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    return send_file(pdf_output, download_name="qr_code_document.pdf", as_attachment=True)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8000))  # Use the PORT environment variable
    app.run(host='0.0.0.0', port=port, debug=True)
