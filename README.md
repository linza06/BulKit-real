# BulkiT – Bulk Certificate Generator

## Team Members  
Member 1: Linsa Biji – MITS 

## Hosted Project Link  
[https://bulkitt.onrender.com]

## Project Description  
BulkiT is a web application that generates certificates in bulk by taking a template image and an Excel/CSV file containing user details.

## The Problem Statement  
Generating certificates manually for large groups is time-consuming and error-prone when only names or a few fields change.

## The Solution  
BulkiT automates certificate creation by allowing users to upload a template and a list of names, and then generating all certificates automatically in bulk.

## Technical Details  

### Technologies/Components Used  

#### For Software:  
Languages used: Python, HTML, CSS  
Frameworks used: Flask  
Libraries used: Pandas, Pillow  
Tools used: VS Code, Git, GitHub  

## Features  
Feature 1: Bulk certificate generation
Feature 2: Live certificate preview
Feature 3: Customize font style
Feature 4: Adjust font size
Feature 5: Change font color
Feature 6: Modify text position 
Feature 7: Download generated certificates in prefered format

## Implementation  

### For Software:  

#### Installation  
```bash
pip install flask pandas pillow
```
###Run
```bash
python app.py
```

## Project Documentation
### For Software:

<img width="1887" height="815" alt="Screenshot 2026-02-21 071558" src="https://github.com/user-attachments/assets/bb9d9edb-dc70-49c9-a718-3f3bdbfd27e6" />
This is the landing Page of the site.

<img width="1888" height="829" alt="Screenshot 2026-02-21 072621" src="https://github.com/user-attachments/assets/669cb4f4-38cf-4b4c-b0b2-bd325ea8c9e0" />
This is where you can customize the font and arrange the position.

<img width="1895" height="829" alt="image" src="https://github.com/user-attachments/assets/1b8ed551-612d-404a-8c81-1b8612d6be34" />
You can preview the file before downloading it.




### Diagrams
        ┌─────────────────────┐
        │        Start        │
        └─────────┬───────────┘
                  │
                  ▼
        ┌─────────────────────┐
        │  User Opens Web App │
        └─────────┬───────────┘
                  │
                  ▼
        ┌────────────────────────────┐
        │ Upload Certificate Template│
        │     (Image: JPG/PNG)       │
        └─────────┬──────────────────┘
                  │
                  ▼
        ┌────────────────────────────┐
        │ Upload Names File          │
        │ (CSV / Excel File)         │
        └─────────┬──────────────────┘
                  │
                  ▼
        ┌────────────────────────────┐
        │  Flask Backend Receives    │
        │        Files               │
        └─────────┬──────────────────┘
                  │
                  ▼
        ┌────────────────────────────┐
        │  Pandas Reads CSV/Excel    │
        │  Extracts List of Names    │
        └─────────┬──────────────────┘
                  │
                  ▼
        ┌────────────────────────────┐
        │ For Each Name:             │
        │  → Open Template (Pillow)  │
        │  → Add Name Text           │
        │  → Save Certificate        │
        └─────────┬──────────────────┘
                  │
                  ▼
        ┌────────────────────────────┐
        │  Store Generated Files     │
        │   (PDF / PNG Format)       │
        └─────────┬──────────────────┘
                  │
                  ▼
        ┌────────────────────────────┐
        │ Provide Download Option    │
        │ (Single / ZIP File)        │
        └─────────┬──────────────────┘
                  │
                  ▼
        ┌─────────────────────┐
        │        End          │
        └─────────────────────┘

  ## Project Demo
  [https://drive.google.com/file/d/1AQf-jYH366gzzecsFzKFZDzECQFGwYD8/view?usp=drive_link]



