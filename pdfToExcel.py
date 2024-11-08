import os
from pdf2image import convert_from_path
import pytesseract
import pandas as pd
import re
from datetime import datetime
from itertools import zip_longest

def calculate_age(birthdate):
    today = datetime.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

def pdf_to_text_with_ocr(folder_path):
    ages = []
    marital = []
    trip_purpose = []
    nationality = []
    occupation = []
    salary = []
    work_description = []
    education_experience = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            images = convert_from_path(pdf_path)

            for i, image in enumerate(images):
                text = pytesseract.image_to_string(image, config='--psm 6')

                # Se obtiene la sección Personal, Address, Phone, and Passport/Travel Document Information 
                # para sacar la fecha de nacimiento y la nacionalidad, ya que estos datos se repiten en otras secciones
                personal_info_match = re.search(r"Personal, Address, Phone, and Passport/Travel Document Information.*", text, re.DOTALL)
                if personal_info_match is not None:
                    personal_info_text = personal_info_match.group(0)
                    dob_match = re.search(r"Date of Birth:\s*(\d{2}\s+[A-Z]+\s+\d{4})", personal_info_text)
                    if dob_match is not None:
                        birthdate = datetime.strptime(dob_match.group(1).strip(), '%d %B %Y')
                        age = calculate_age(birthdate)
                        ages.append(age)

                    nationality_match = re.search(r"Country/Region of Origin \(Nationality\):\s*(.*)", personal_info_text)
                    if nationality_match is not None:
                        nationality.append(nationality_match.group(1).strip())

                marital_match = re.search(r"Marital Status:\s*(.*)", text)
                if marital_match is not None:
                    marital.append(marital_match.group(1).strip())

                purpose_match = re.search(r"Purpose of Trip to the U.S. \(1\):\s*(.*)", text)
                if purpose_match is not None:
                    trip_purpose.append(purpose_match.group(1).strip())

                ocupation_match = re.search(r"Primary Occupation:\s*(.*)", text)
                if ocupation_match is not None:
                    occupation.append(ocupation_match.group(1).strip())

                salary_match = re.search(r"Monthly Salary in Local Currency \(if employed\):\s*(.*)", text)
                if salary_match is not None:
                    salary.append(salary_match.group(1).strip())

                work_match = re.search(r"Briefly Describe your Duties:\s*(.*)", text)
                if work_match is not None:
                    work_description.append(work_match.group(1).strip())

                education_matches = re.findall(r"Course of Study:\s*(.*)", text)
                if education_matches is not None and len(education_matches) > 0:
                    cadena_courses = ""
                    for education in education_matches:
                        cadena_courses = cadena_courses + education
                        if education != education_matches[-1]:
                            cadena_courses = cadena_courses + ", "
                    education_experience.append(cadena_courses)
                    
    # Este código lo que hace es transponer espacios en blanco en los arrays para que todos los arrays sean del mismo tamaño
    # y asi evitar este error de Pandas: ValueError: arrays must all be same length
    arrays = [ages, marital, trip_purpose,nationality, occupation, salary, work_description, education_experience]
    max_length = max(len(arr) for arr in arrays)
    arrays_padded = [arr + [None] * (max_length - len(arr)) for arr in arrays]
    df = pd.DataFrame(arrays_padded).T
    return df

def save_text_to_excel(df, output_excel_path):
    df = pd.DataFrame({"Age": df[0],
                       "Marital Status": df[1],
                       "Purpose of Trip to the U.S.": df[2],
                       "Nationality": df[3],
                       "Primary Occupation": df[4],
                       "Monthly Salary": df[5],
                       "Work Description": df[6],
                       "Education": df[7]})
    df.to_excel(output_excel_path, index=False)

folder_path = '/Users/natalia.marin/Documents/HojasVidaPdf'
df = pdf_to_text_with_ocr(folder_path)
output_excel_path = '/Users/natalia.marin/Documents/HV16.xlsx'
save_text_to_excel(df, output_excel_path)