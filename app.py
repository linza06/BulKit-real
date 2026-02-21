import os
import uuid
import pandas as pd
from flask import Flask, render_template, request, send_file, url_for, jsonify
from PIL import Image, ImageDraw, ImageFont
import zipfile

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
GENERATED_FOLDER = "generated"
PREVIEW_FOLDER = "static/previews"
FONTS_FOLDER = "static/fonts"

for folder in [UPLOAD_FOLDER, GENERATED_FOLDER, PREVIEW_FOLDER, FONTS_FOLDER]:
    os.makedirs(folder, exist_ok=True)

def draw_certificate(template_path, name, y_pos, font_size, color, font_name):
    image = Image.open(template_path).convert("RGB")
    draw = ImageDraw.Draw(image)
    width, height = image.size
    try:
        font = ImageFont.truetype(os.path.join(FONTS_FOLDER, font_name), font_size)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), name, font=font)
    x = (width - (bbox[2] - bbox[0])) / 2
    draw.text((x, y_pos), name, fill=color, font=font)
    return image

def convert_to_format(image, export_format):
    """Convert PIL image to specified format"""
    if export_format.lower() == "pdf":
        return image.convert("RGB")
    elif export_format.lower() in ("jpg", "jpeg"):
        return image.convert("RGB")
    else:  # PNG
        return image.convert("RGBA")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_fonts", methods=["GET"])
def get_fonts():
    try:
        fonts = [f for f in os.listdir(FONTS_FOLDER) if f.endswith('.ttf') or f.endswith('.TTF')]
        if not fonts:
            fonts = ["arial.ttf"]
        return jsonify({"fonts": sorted(fonts)})
    except Exception as e:
        return jsonify({"fonts": ["arial.ttf"], "error": str(e)})

def choose_template_for_status(status, paths, has_first=False, has_second=False, has_third=False):
    s = (status or "").strip().lower()
    if has_first and (s in ("1","1st","first","winner") or "1st" in s or "first" in s or "winner" in s):
        return paths.get("first")
    if has_second and (s in ("2","2nd","second") or "2nd" in s or "second" in s):
        return paths.get("second")
    if has_third and (s in ("3","3rd","third") or "3rd" in s or "third" in s):
        return paths.get("third")
    return paths.get("participant")

@app.route("/preview", methods=["POST"])
def preview():
    first_temp = request.files.get("first_template")
    second_temp = request.files.get("second_template")
    third_temp = request.files.get("third_template")
    participant_temp = request.files.get("participant_template")
    csv_file = request.files.get("csv")
    all_participants = request.form.get("all_participants") == "on"

    if not (participant_temp or first_temp or second_temp or third_temp):
        return jsonify({"error": "Upload at least one template (participant or place templates)."}), 400
    if not csv_file:
        return jsonify({"error": "Upload an Excel/CSV file for preview."}), 400

    saved = {}
    csv_path = None
    try:
        if first_temp:
            p = os.path.join(UPLOAD_FOLDER, "preview_first_" + first_temp.filename); first_temp.save(p); saved["first"] = p
        if second_temp:
            p = os.path.join(UPLOAD_FOLDER, "preview_second_" + second_temp.filename); second_temp.save(p); saved["second"] = p
        if third_temp:
            p = os.path.join(UPLOAD_FOLDER, "preview_third_" + third_temp.filename); third_temp.save(p); saved["third"] = p
        if participant_temp:
            p = os.path.join(UPLOAD_FOLDER, "preview_part_" + participant_temp.filename); participant_temp.save(p); saved["participant"] = p

        csv_path = os.path.join(UPLOAD_FOLDER, "preview_" + csv_file.filename); csv_file.save(csv_path)
        df = pd.read_csv(csv_path) if csv_path.endswith('.csv') else pd.read_excel(csv_path)
        if df.shape[0] == 0:
            raise ValueError("CSV/Excel is empty.")
        name = str(df.iloc[0, 0]).strip().upper()
        status = "" if all_participants else (str(df.iloc[0, 1]) if df.shape[1] > 1 else "")

        has_first = request.form.get("has_first") == "on"
        has_second = request.form.get("has_second") == "on"
        has_third = request.form.get("has_third") == "on"

        if all_participants:
            chosen = saved.get("participant") or saved.get("first") or saved.get("second") or saved.get("third")
        else:
            chosen = choose_template_for_status(status, saved, has_first, has_second, has_third)

        if not chosen:
            raise ValueError("Appropriate template not provided for preview.")

        y_pos = int(request.form.get("y_pos", 450))
        font_size = int(request.form.get("font_size", 80))
        color = request.form.get("color", "#ffffff")
        font_name = request.form.get("font_name", "arial.ttf")

        # Draw certificate using actual template
        cert = draw_certificate(chosen, name, y_pos, font_size, color, font_name)
        export_format = request.form.get("export_format", "png").lower()
        cert = convert_to_format(cert, export_format)
        
        preview_name = f"preview_{uuid.uuid4().hex[:6]}.png"
        preview_path = os.path.join(PREVIEW_FOLDER, preview_name)
        cert.save(preview_path)
        return jsonify({"preview_url": url_for('static', filename=f'previews/{preview_name}')})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        for p in saved.values():
            try: os.remove(p)
            except: pass
        try:
            if csv_path: os.remove(csv_path)
        except: pass

@app.route("/upload", methods=["POST"])
def upload():
    first_temp = request.files.get("first_template")
    second_temp = request.files.get("second_template")
    third_temp = request.files.get("third_template")
    participant_temp = request.files.get("participant_template")
    csv_file = request.files.get("csv")
    all_participants = request.form.get("all_participants") == "on"
    has_first = request.form.get("has_first") == "on"
    has_second = request.form.get("has_second") == "on"
    has_third = request.form.get("has_third") == "on"
    export_format = request.form.get("export_format", "png").lower()

    if not (participant_temp or first_temp or second_temp or third_temp):
        return "Upload at least one template (participant or place templates).", 400
    if not csv_file:
        return "Upload an Excel/CSV file.", 400

    y_pos = int(request.form.get("y_pos", 450))
    font_size = int(request.form.get("font_size", 80))
    color = request.form.get("color", "#ffffff")
    font_name = request.form.get("font_name", "arial.ttf")

    paths = {}
    if first_temp:
        p = os.path.join(UPLOAD_FOLDER, "first_" + first_temp.filename); first_temp.save(p); paths["first"] = p
    if second_temp:
        p = os.path.join(UPLOAD_FOLDER, "second_" + second_temp.filename); second_temp.save(p); paths["second"] = p
    if third_temp:
        p = os.path.join(UPLOAD_FOLDER, "third_" + third_temp.filename); third_temp.save(p); paths["third"] = p
    if participant_temp:
        p = os.path.join(UPLOAD_FOLDER, "participant_" + participant_temp.filename); participant_temp.save(p); paths["participant"] = p

    csv_path = os.path.join(UPLOAD_FOLDER, csv_file.filename); csv_file.save(csv_path)

    try:
        df = pd.read_csv(csv_path) if csv_path.endswith('.csv') else pd.read_excel(csv_path)
    except Exception as e:
        return f"Error reading file: {e}", 400

    if df.shape[0] == 0 or df.shape[1] < 1:
        return "CSV/Excel must have at least one column with names.", 400

    zip_name = f"final_certs_{uuid.uuid4().hex[:6]}.zip"
    zip_path = os.path.join(GENERATED_FOLDER, zip_name)

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for i, row in df.iterrows():
            try:
                name = str(row.iloc[0]).strip().upper()
                status = "" if all_participants else (str(row.iloc[1]) if df.shape[1] > 1 else "")
                if all_participants:
                    chosen = paths.get("participant") or paths.get("first") or paths.get("second") or paths.get("third")
                else:
                    chosen = choose_template_for_status(status, paths, has_first, has_second, has_third)
                    if not chosen:
                        chosen = paths.get("participant") or paths.get("first") or paths.get("second") or paths.get("third")
                if not chosen:
                    continue
                cert = draw_certificate(chosen, name, y_pos, font_size, color, font_name)
                cert = convert_to_format(cert, export_format)
                
                img_name = f"{i+1}_{name.replace(' ', '_')}.{export_format}"
                img_path = os.path.join(GENERATED_FOLDER, img_name)
                cert.save(img_path)
                zipf.write(img_path, img_name)
                os.remove(img_path)
            except Exception:
                continue

    for v in paths.values():
        try: os.remove(v)
        except: pass
    try: os.remove(csv_path)
    except: pass

    return send_file(zip_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=int(os.environ.get("PORT", 4000)))
