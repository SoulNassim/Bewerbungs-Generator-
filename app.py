from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import json
import datetime
import base64
import tempfile
from dotenv import load_dotenv
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, StyleSheet1
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_RIGHT, TA_LEFT, TA_CENTER
from PyPDF2 import PdfReader
import io

load_dotenv()

app = Flask(__name__)
CORS(app)

PROFILE_DIR = "profiles"
if not os.path.exists(PROFILE_DIR):
    os.makedirs(PROFILE_DIR)

# Lazy load OpenAI client to avoid compatibility issues
client = None

def get_openai_client():
    global client
    if client is None:
        try:
            import httpx
            from openai import OpenAI
            
            # Workaround for Python 3.14 compatibility issues
            # Create custom httpx client without problematic arguments
            http_client = httpx.Client()
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), http_client=http_client)
        except Exception as e:
            print(f"Warning: Could not initialize OpenAI client: {e}")
            # Try fallback approach
            try:
                from openai import OpenAI
                client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            except Exception as e2:
                print(f"Fallback also failed: {e2}")
                return None
    return client

def get_profiles():
    """Get all saved profiles"""
    profiles = []
    if os.path.exists(PROFILE_DIR):
        for file in os.listdir(PROFILE_DIR):
            if file.endswith(".json"):
                profiles.append(file.replace(".json", ""))
    return profiles

def load_profile(profile_name):
    """Load a profile from JSON"""
    file_path = os.path.join(PROFILE_DIR, f"{profile_name}.json")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_profile(profile_name, data):
    """Save a profile to JSON"""
    file_path = os.path.join(PROFILE_DIR, f"{profile_name}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def extract_cv_text(file_path):
    """Extract text from PDF or TXT file"""
    try:
        text = ""
        if file_path.lower().endswith(".pdf"):
            reader = PdfReader(file_path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        elif file_path.lower().endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        return text
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def generate_cover_letter_ai(job_title, company, cv_text, style_prompt):
    """Generate cover letter using OpenAI API"""
    client = get_openai_client()
    if not client:
        return "Error: OpenAI API not configured. Please check your OPENAI_API_KEY in .env"
    
    prompt = f"""Generate a professional German cover letter (Bewerbungsschreiben) for this position:
    
Job Title: {job_title}
Company: {company}

CV/Background: {cv_text[:1000]}

Style instruction: {style_prompt}

Format the response as:
Subject: [Betreff]

[Cover letter body - 3 paragraphs. Keep it slightly more concise and space-saving than usual (around 250 words), ensuring it comfortably fits on a single A4 page without being overly short.]

IMPORTANT: Do NOT include any closing phrase (like "Mit freundlichen Grüßen", "Grüße", or "MfG"). Only generate the subject line and body paragraphs. The closing will be added automatically by the template."""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional German cover letter writer. You write eloquent cover letters that perfectly fit on one page without being excessively long."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=600
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating cover letter: {str(e)}"

def create_pdf_from_template(user_data, cover_letter_text, signature_path=None, layout='classic', font_name='Helvetica'):
    """Create a PDF with the cover letter using the specified layout"""
    try:
        output = io.BytesIO()
        doc = SimpleDocTemplate(output, pagesize=A4, rightMargin=2.5*cm, leftMargin=2.5*cm, topMargin=2*cm, bottomMargin=2*cm)
        
        # Map font names to ReportLab fonts
        font_map = {
            'Helvetica': 'Helvetica',
            'Times': 'Times-Roman',
            'Courier': 'Courier',
            'Georgia': 'Times-Roman',  # Fallback
        }
        font = font_map.get(font_name, 'Helvetica')
        
        # Create fresh StyleSheet
        from reportlab.lib.styles import StyleSheet1
        styles = StyleSheet1()
        styles.add(ParagraphStyle(name='Normal', fontName=font, fontSize=11, leading=14))
        styles.add(ParagraphStyle(name='RightAlign', fontName=font, fontSize=10, alignment=TA_RIGHT))
        styles.add(ParagraphStyle(name='Address', fontName=font, fontSize=10, leading=12))
        styles.add(ParagraphStyle(name='Header', fontName=font, fontSize=12, alignment=TA_CENTER, spaceAfter=12))
        styles.add(ParagraphStyle(name='Separator', fontName=font, fontSize=8))
        
        # Escape special characters in cover letter
        safe_letter = cover_letter_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        safe_letter = safe_letter.replace('\n\n', '<br/><br/>').replace('\n', ' ')
        
        def format_custom(key):
            raw = user_data.get(key)
            if not raw:
                return None
            safe = raw.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            return safe.replace('\n', '<br/>')
            
        custom_header = format_custom('custom_header')
        custom_recipient = format_custom('custom_recipient')
        custom_date = format_custom('custom_date')
        custom_greeting = format_custom('custom_greeting')

        today = custom_date or datetime.date.today().strftime("%d. %B %Y")
        
        story = []
        
        if layout == 'modern':
            if custom_header:
                 story.append(Paragraph(custom_header, styles['Header']))
            else:
                 header = f"{user_data.get('name', '')} | {user_data.get('email', '')} | {user_data.get('phone', '')}"
                 story.append(Paragraph(header, styles['Header']))
                 story.append(Paragraph(f"{user_data.get('street', '')} • {user_data.get('city', '')}", styles['Normal']))
            
            story.append(Paragraph("─────────────────────────────────────────", styles['Separator']))
            story.append(Spacer(1, 0.5*cm))
            
            if custom_recipient:
                 story.append(Paragraph(custom_recipient, styles['Address']))
            else:
                 recipient = f"{user_data.get('company', '')}<br/>{user_data.get('company_street', '')}<br/>{user_data.get('company_city', '')}"
                 story.append(Paragraph(recipient, styles['Address']))
                 
            story.append(Spacer(1, 0.5*cm))
            story.append(Paragraph(today, styles['RightAlign']))
            story.append(Spacer(1, 0.5*cm))
            
        elif layout == 'minimal':
            story.append(Paragraph(today, styles['RightAlign']))
            story.append(Spacer(1, 0.5*cm))
            
            if custom_recipient:
                 story.append(Paragraph(custom_recipient, styles['Address']))
            else:
                 recipient = f"{user_data.get('company', '')}<br/>{user_data.get('company_street', '')}"
                 story.append(Paragraph(recipient, styles['Address']))
                 
            story.append(Spacer(1, 0.5*cm))
            
        elif layout == 'compact':
            if custom_header:
                 story.append(Paragraph(custom_header, styles['Normal']))
            else:
                 header = f"{user_data.get('name', '')} • {user_data.get('street', '')} • {user_data.get('city', '')}"
                 story.append(Paragraph(header, styles['Normal']))
                 story.append(Paragraph(f"{user_data.get('email', '')} | {user_data.get('phone', '')}", styles['Normal']))
                 
            story.append(Spacer(1, 0.5*cm))
            
            if custom_recipient:
                 story.append(Paragraph(custom_recipient, styles['Normal']))
            else:
                 company_header = f"{user_data.get('company', '')} | {user_data.get('company_street', '')}"
                 story.append(Paragraph(company_header, styles['Normal']))
                 
            story.append(Paragraph(today, styles['RightAlign']))
            story.append(Spacer(1, 0.5*cm))
            
        else:  # classic/default
            if custom_header:
                 story.append(Paragraph(custom_header, styles['RightAlign']))
            else:
                 sender_lines = [
                     user_data.get('name', ''),
                     user_data.get('street', ''),
                     user_data.get('city', ''),
                     user_data.get('email', ''),
                     user_data.get('phone', '')
                 ]
                 sender_text = '<br/>'.join([line.strip() for line in sender_lines if line.strip()])
                 story.append(Paragraph(sender_text, styles['RightAlign']))
                 
            story.append(Spacer(1, 1.5*cm))
            
            if custom_recipient:
                 story.append(Paragraph(custom_recipient, styles['Address']))
            else:
                 recipient_lines = [
                     user_data.get('company', ''),
                     user_data.get('company_street', ''),
                     user_data.get('company_city', '')
                 ]
                 recipient_text = '<br/>'.join([line.strip() for line in recipient_lines if line.strip()])
                 story.append(Paragraph(recipient_text, styles['Address']))
                 
            story.append(Spacer(1, 1*cm))
            story.append(Paragraph(today, styles['RightAlign']))
            story.append(Spacer(1, 0.5*cm))
        
        # Add cover letter content
        story.append(Paragraph(safe_letter, styles['Normal']))
        story.append(Spacer(1, 1*cm))
        
        # Add closing
        if custom_greeting:
             story.append(Paragraph(custom_greeting, styles['Normal']))
        else:
             if layout == 'minimal':
                 story.append(Paragraph("Grüße,", styles['Normal']))
             elif layout == 'compact':
                 story.append(Paragraph("MfG,", styles['Normal']))
             else:
                 story.append(Paragraph("Mit freundlichen Grüßen,", styles['Normal']))
        
        story.append(Spacer(1, 0.4*cm))
        
        # Signature
        if signature_path and os.path.exists(signature_path):
            try:
                sig_scale = float(user_data.get('sig_scale', 1))
                sig_indent = float(user_data.get('sig_indent', 0))
                
                img_width = 4*cm * sig_scale
                img_height = 1.5*cm * sig_scale
                img = Image(signature_path, width=img_width, height=img_height, kind='proportional')
                img.hAlign = 'LEFT'
                
                if sig_indent > 0:
                    t = Table([['', img]], colWidths=[sig_indent, img_width])
                    story.append(t)
                else:
                    story.append(img)
            except Exception as sig_err:
                print(f"Warning: Could not add signature: {sig_err}")
                
        doc.build(story)
        output.seek(0)
        return output
    except Exception as e:
        print(f"PDF Generation Error: {e}")
        import traceback
        traceback.print_exc()
        raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/profiles', methods=['GET'])
def get_profiles_api():
    return jsonify({"profiles": get_profiles()})

@app.route('/api/profile/<name>', methods=['GET'])
def get_profile_api(name):
    profile = load_profile(name)
    if profile:
        return jsonify(profile)
    return jsonify({"error": "Profile not found"}), 404

@app.route('/api/profile/<name>', methods=['POST'])
def save_profile_api(name):
    data = request.json
    save_profile(name, data)
    return jsonify({"success": True, "message": f"Profile '{name}' saved"})

@app.route('/api/delete-profile/<name>', methods=['DELETE'])
def delete_profile_api(name):
    file_path = os.path.join(PROFILE_DIR, f"{name}.json")
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"success": True})
    return jsonify({"error": "Profile not found"}), 404

@app.route('/api/extract-cv', methods=['POST'])
def extract_cv():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Save file temporarily
    temp_path = os.path.join("temp", file.filename)
    os.makedirs("temp", exist_ok=True)
    file.save(temp_path)
    
    text = extract_cv_text(temp_path)
    os.remove(temp_path)
    
    return jsonify({"cv_text": text})

@app.route('/api/generate-application', methods=['POST'])
def generate_application():
    data = request.json
    
    try:
        # Generate cover letter
        cover_letter = generate_cover_letter_ai(
            data['job_title'],
            data['company'],
            data.get('cv_text', ''),
            data.get('style_prompt', 'Schreibe professionell und überzeugend.')
        )
        
        return jsonify({"cover_letter": cover_letter})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate-pdf', methods=['POST'])
def generate_pdf():
    data = request.json
    
    try:
        # Validate required data
        required_fields = ['name', 'street', 'city', 'email', 'phone', 'company', 'cover_letter']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"Missing field: {field}"}), 400
        
        layout = data.get('layout', 'classic')
        font = data.get('font', 'Helvetica')
        
        sig_path = None
        sig_base64 = data.get('signature_base64')
        if sig_base64:
            try:
                encoded_data = sig_base64.split(",")[1] if "," in sig_base64 else sig_base64
                img_data = base64.b64decode(encoded_data)
                fd, temp_path = tempfile.mkstemp(suffix='.png')
                with open(fd, 'wb') as f:
                    f.write(img_data)
                sig_path = temp_path
            except Exception as e:
                print(f"Signature processing error: {e}")
        
        pdf_bytes = create_pdf_from_template(
            {
                'name': data.get('name', ''),
                'street': data.get('street', ''),
                'city': data.get('city', ''),
                'email': data.get('email', ''),
                'phone': data.get('phone', ''),
                'company': data.get('company', ''),
                'company_street': data.get('company_street', ''),
                'company_city': data.get('company_city', ''),
                'custom_header': data.get('custom_header', ''),
                'custom_recipient': data.get('custom_recipient', ''),
                'custom_date': data.get('custom_date', ''),
                'custom_greeting': data.get('custom_greeting', ''),
                'sig_scale': data.get('sig_scale', 1),
                'sig_indent': data.get('sig_indent', 0)
            },
            data.get('cover_letter', ''),
            sig_path or data.get('signature_path'),
            layout=layout,
            font_name=font
        )
        
        if sig_path and os.path.exists(sig_path):
            try:
                os.remove(sig_path)
            except:
                pass
        
        return send_file(
            pdf_bytes, 
            mimetype='application/pdf', 
            as_attachment=True, 
            download_name='Bewerbung.pdf'
        )
    except Exception as e:
        print(f"PDF Generation Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"PDF generation failed: {str(e)}"}), 500

@app.route('/api/preview-pdf', methods=['POST', 'GET'])
def preview_pdf():
    """Generate and return PDF for preview (not as attachment)"""
    
    # Handle both POST (JSON) and GET (query parameters)
    if request.method == 'GET':
        data = {
            'name': request.args.get('name', ''),
            'street': request.args.get('street', ''),
            'city': request.args.get('city', ''),
            'email': request.args.get('email', ''),
            'phone': request.args.get('phone', ''),
            'company': request.args.get('company', ''),
            'company_street': request.args.get('company_street', ''),
            'company_city': request.args.get('company_city', ''),
            'cover_letter': request.args.get('cover_letter', ''),
            'layout': request.args.get('layout', 'classic'),
            'font': request.args.get('font', 'Helvetica'),
        }
    else:
        data = request.json
    
    try:
        # Validate required data
        required_fields = ['name', 'street', 'city', 'email', 'phone', 'company', 'cover_letter']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"Missing field: {field}"}), 400
        
        layout = data.get('layout', 'classic')
        font = data.get('font', 'Helvetica')
        
        pdf_bytes = create_pdf_from_template(
            {
                'name': data.get('name', ''),
                'street': data.get('street', ''),
                'city': data.get('city', ''),
                'email': data.get('email', ''),
                'phone': data.get('phone', ''),
                'company': data.get('company', ''),
                'company_street': data.get('company_street', ''),
                'company_city': data.get('company_city', ''),
            },
            data.get('cover_letter', ''),
            data.get('signature_path'),
            layout=layout,
            font_name=font
        )
        
        return send_file(
            pdf_bytes, 
            mimetype='application/pdf',
            as_attachment=False  # Display inline, not as download
        )
    except Exception as e:
        print(f"PDF Preview Generation Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"PDF generation failed: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
