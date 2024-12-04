import os
from pdf2image import convert_from_path
import pytesseract
import pandas as pd
import re
from datetime import datetime

def calculate_age(birthdate):
    today = datetime.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

def pdf_to_text_with_ocr(folder_path):
    # Inicializar listas para cada campo
    ages = []
    marital = []
    trip_purpose = []
    nationality = []
    occupation = []
    salary = []
    work_description = []
    education_experience = []
    countries_visited = []
    refuse_visa = []
    mother_in_us = []
    immediate_relatives = []
    other_relatives = []
    cancelled_revoked_visa = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            images = convert_from_path(pdf_path)
            
            # Variables para almacenar datos de una fila (PDF)
            age, marital_status, trip_purpose_val, nationality_val = "N/A", "N/A", "N/A", "N/A"
            occupation_val, salary_val, work_description_val = "OTHER", "No tiene", "No tiene"
            education_experience_val, countries_visited_val = "No tiene", "No ha viajado"
            refuse_visa_val, mother_in_us_val, immediate_relatives_val, other_relatives_val = "N/A", "N/A", "N/A", "NO"
            cancelled_revoked_visa_val = "No aplica"
            
            # Procesar cada imagen del PDF
            for i, image in enumerate(images):
                text = pytesseract.image_to_string(image, config='--psm 6')

                # Extraer información relevante usando expresiones regulares
                personal_info_match = re.search(r"Personal, Address, Phone, and Passport/Travel Document Information.*", text, re.DOTALL)
                work_ed_train_info_match = re.search(r"Work/Education/Training Information.*", text, re.DOTALL)

                if personal_info_match is not None:
                    personal_info_text = personal_info_match.group(0)
                    dob_match = re.search(r"Date of Birth:\s*(\d{2}\s+[A-Z]+\s+\d{4})", personal_info_text)
                    if dob_match is not None:
                        birthdate = datetime.strptime(dob_match.group(1).strip(), '%d %B %Y')
                        age = calculate_age(birthdate)

                    nationality_match = re.search(r"Country/Region of Origin \(Nationality\):\s*(.*)", personal_info_text)
                    if nationality_match is not None:
                        nationality_val = nationality_match.group(1).strip()

                marital_match = re.search(r"Marital Status:\s*(.*)", text)
                if marital_match is not None:
                    marital_status = marital_match.group(1).strip()

                purpose_match = re.search(r"Purpose of Trip to the U.S. \(1\):\s*(.*)", text)
                if purpose_match is not None:
                    trip_purpose_val = purpose_match.group(1).strip()

                if work_ed_train_info_match is not None:
                    ocupation_match = re.search(r"Primary Occupation:\s*(.*)", text)
                    if ocupation_match is not None:
                        occupation_val = ocupation_match.group(1).strip()

                salary_match = re.search(r"Monthly Salary in Local Currency \(if employed\):\s*(.*)", text)
                if salary_match is not None:
                    salary_val = salary_match.group(1).strip()

                work_match = re.search(r"Briefly Describe your Duties:\s*(.*)", text)
                if work_match is not None:
                    work_description_val = work_match.group(1).strip()

                education_matches = re.findall(r"Course of Study:\s*(.*)", text)
                if education_matches:
                    education_experience_val = ", ".join(education_matches)
                    
                travel_five_years_match = re.search(r"Have you traveled to any countries/regions within the last five years?\s*(.*)", text) 
                if travel_five_years_match is not None:
                    country_region_matches = re.findall(r"Country/Region \(\d+\):\s*(.*)", text)
                    countries_visited_val = ", ".join(country_region_matches) if country_region_matches else "No ha viajado"
                
                refuse_visa_match = re.search(r"Have you ever been refused a U.S. Visa, or been refused admission to\s*(.*)", text)
                if refuse_visa_match is not None:
                    refuse_visa_val = refuse_visa_match.group(1).strip()
                    
                mother_in_us_match = re.search(r"Is your mother in the U.S.\?\s*(.*)", text)
                if mother_in_us_match is not None:
                    mother_in_us_val = mother_in_us_match.group(1).strip()
                    
                immediate_relatives_match = re.search(r"Do you have any immediate relatives, not including parents in the U.S.\?\s*(.*)", text)
                if immediate_relatives_match is not None:
                    immediate_relatives_val = immediate_relatives_match.group(1).strip()
                    
                other_relatives_match = re.search(r"Do you have any other relatives in the United States\?\s*(.*)", text)
                if other_relatives_match is not None:
                    other_relatives_val = other_relatives_match.group(1).strip()

                # Nueva búsqueda para la pregunta sobre visa cancelada o revocada con un regex flexible
                cancelled_revoked_visa_match = re.search(r"Has your U\.S\. Visa ever been cancelled or revoked\?\s*(YES|NO)", text, re.IGNORECASE)
                if cancelled_revoked_visa_match is not None:
                    cancelled_revoked_visa_val = cancelled_revoked_visa_match.group(1).strip()

            # Agregar la información del PDF procesado a las listas
            ages.append(age)
            marital.append(marital_status)
            trip_purpose.append(trip_purpose_val)
            nationality.append(nationality_val)
            occupation.append(occupation_val)
            salary.append(salary_val)
            work_description.append(work_description_val)
            education_experience.append(education_experience_val)
            countries_visited.append(countries_visited_val)
            refuse_visa.append(refuse_visa_val)
            mother_in_us.append(mother_in_us_val)
            immediate_relatives.append(immediate_relatives_val)
            other_relatives.append(other_relatives_val)
            cancelled_revoked_visa.append(cancelled_revoked_visa_val)
                                    
    # Crear el DataFrame sin añadir filas adicionales
    df = pd.DataFrame({
        "Age": ages,
        "Marital Status": marital,
        "Purpose of Trip to the U.S.": trip_purpose,
        "Nationality": nationality,
        "Primary Occupation": occupation,
        "Monthly Salary": salary,
        "Work Description": work_description,
        "Education": education_experience,
        "Visited Countries": countries_visited,
        "Have you ever been refused a U.S. Visa?": refuse_visa,
        "Is your mother in the U.S.?": mother_in_us,
        "Do you have any immediate relatives, not including parents in the U.S.?": immediate_relatives,
        "Do you have any other relatives in the United States?": other_relatives,
        "Has your U.S. Visa ever been cancelled or revoked?": cancelled_revoked_visa
    })
    return df

def save_text_to_excel(df, output_excel_path):
    df.to_excel(output_excel_path, index=False)

# PROCESAMIENTO DE DATOS
folder_path = '/Users/natalia.marin/Documents/HojasVidaPdf'
df = pdf_to_text_with_ocr(folder_path)
output_excel_path = '/Users/natalia.marin/Documents/HV1.xlsx'
save_text_to_excel(df, output_excel_path)

df = pdf_to_text_with_ocr(folder_path)
save_text_to_excel(df, output_excel_path)
