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

    # QR kod yarat
    qr = qrcode.make(qr_data)
    qr_buffer = BytesIO()
    qr.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)

    # PDF faylı yarat
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt=subject, ln=True, align="C")
    qr_image_path = "temp_qr.png"
    with open(qr_image_path, "wb") as f:
        f.write(qr_buffer.getvalue())
    pdf.image(qr_image_path, x=80, y=50, w=50)
    pdf.set_font("Arial", size=12)
    pdf.ln(70)
    pdf.multi_cell(0, 10, txt=content)
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    return send_file(pdf_output, download_name="qr_code_document.pdf", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
