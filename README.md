BulkiT — Bulk Certificate Generator
Generate beautiful certificates in bulk with custom templates, fonts, and positioning.

✨ Features
Multi-template support (1st, 2nd, 3rd place + participant)
Batch process 100+ certificates from CSV/Excel
Real-time preview before download
Export as PNG, JPG, or PDF
Custom fonts and positioning
Drag & drop file upload
📦 Installation
# Install dependencies
pip install flask pillow pandas openpyxl

# Create folders
mkdir uploads generated static/previews static/fonts

# Run app
python app.py
🗂️ Project Structure
BulkiT/
├── app.py              # Flask backend
├── templates/
│   └── index.html      # Frontend UI
├── static/
│   ├── fonts/          # .ttf font files
│   └── previews/       # Generated previews
├── uploads/            # Temp uploaded files
└── generated/          # Output ZIP files
🔄 How It Works
Upload Files → Template images + CSV with names/status
Customize → Adjust font, position, color, size
Preview → See first certificate before batch
Download → Get ZIP with all certificates
📚 Key Functions
Backend (app.py)
Function	Purpose
draw_certificate()	Draw name on template image
choose_template_for_status()	Select template based on status
GET /get_fonts	List available fonts
POST /preview	Generate single preview
POST /upload	Generate & download all certificates
Frontend (JavaScript)
Function	Purpose
loadFonts()	Fetch fonts from backend
updatePreview()	Generate live preview
debounce()	Prevent excessive calls
📖 Quick Start
CSV Format
Name,Status
John Doe,1st
Jane Smith,2nd
Bob Johnson,Null
Steps
Create CSV with names in Column 1, status in Column 2
Upload participant template (required)
Upload other templates (optional) and check boxes
Adjust Y-Position and Font Size
Click "Preview" to test
Click "Download ZIP"
📦 Dependencies
Flask — Web framework
Pillow — Image processing
Pandas — CSV/Excel handling
Tailwind CSS — Frontend styling (CDN)
