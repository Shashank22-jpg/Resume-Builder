from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ---------------- CONFIG ----------------
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ---------------- HOME ----------------
@app.route('/')
def index():
    return render_template('index.html')


# ---------------- PREVIEW ----------------
@app.route('/preview', methods=['POST'])
def preview():
    file = request.files.get('photo')
    filepath = ""

    if file and file.filename != "":
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

    data = {
        "name": request.form.get('name'),
        "email": request.form.get('email'),
        "phone": request.form.get('phone'),
        "skills": request.form.get('skills'),
        "education": request.form.get('education'),
        "experience": request.form.get('experience'),
        "photo": filepath
    }

    # Template selection
    template = request.form.get('template', 'template1')

    return render_template(f"{template}.html", data=data)


# ---------------- PDF DOWNLOAD ----------------
@app.route('/download', methods=['POST'])
def download():
    data = request.form

    pdf_path = "resume.pdf"
    c = canvas.Canvas(pdf_path)

    # Name
    c.setFont("Helvetica-Bold", 18)
    c.drawString(200, 800, data.get('name', ''))

    # Contact
    c.setFont("Helvetica", 12)
    c.drawString(50, 760, f"Email: {data.get('email', '')}")
    c.drawString(50, 740, f"Phone: {data.get('phone', '')}")

    # Skills
    c.drawString(50, 700, "Skills:")
    c.drawString(50, 680, data.get('skills', ''))

    # Education
    c.drawString(50, 650, "Education:")
    c.drawString(50, 630, data.get('education', ''))

    # Experience
    c.drawString(50, 600, "Experience:")
    c.drawString(50, 580, data.get('experience', ''))

    c.save()

    return send_file(pdf_path, as_attachment=True)


# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)