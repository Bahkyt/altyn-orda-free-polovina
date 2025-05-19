import random
import sqlite3

from PIL import Image, ImageDraw, ImageFont


def fetch_all_from_db():
    try:
        with sqlite3.connect("olympiad.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")  # Замените 'users' на название вашей таблицы
            rows = cursor.fetchall()  # Получаем все строки
            for row in rows:
                print(row)  # Печатаем каждую строку
    except Exception as e:
        print(f"Ошибка базы данных: {e}")

#fetch_all_from_db()

def init_db():
    with sqlite3.connect("olympiad.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                school_class INTEGER,
                class_letter TEXT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                payment_status INTEGER DEFAULT 0,
                score_1 INTEGER DEFAULT 0,
                score_2 INTEGER DEFAULT 0,
                score_3 INTEGER DEFAULT 0,
                test_date TEXT,
                certificate_path TEXT,
                forgot_password TEXT
            );
        """)
        conn.commit()

#init_db()

def update_db_payment_status(id):
    with sqlite3.connect("olympiad.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users
            SET score_1 = ?
            WHERE id = ?
        """, (0, id))
        conn.commit()

#update_db_payment_status(1)

def generate_certificate(user_id, user_name, user_score):
    try:
        # Имя и фамилия
        full_name = user_name
        x_offset = 860
        y_offset = 535

        # Загружаем фото
        image = Image.open("static/certificate/certificate.png")

        # Создаём объект для рисования
        draw = ImageDraw.Draw(image)

        # Загружаем TTF-шрифт с поддержкой кириллицы
        font_path = "OpenSans-Medium.ttf"  # Положи сюда свой шрифт
        font_size = 50
        font = ImageFont.truetype(font_path, font_size)

        # Позиция — с учётом смещений (x_offset, y_offset)
        x = x_offset
        y = y_offset

        # Нарисовать текст
        draw.text((x, y), full_name, font=font, fill=(0, 0, 0))
        draw.text((800, 750), user_score, font=font, fill=(0, 0, 0))

        # Сохраняем в certificate/1.jpg
        image.save(f"static/certificate/1/certificate.png")

        return f"static/certificate/1/certificate.png"
    except Exception as e:
        print(f"Ошибка генерации: {e}")
        return None

generate_certificate(1, "пк пк", str(1))


import fitz  # PyMuPDF
import os
from PIL import Image
from io import BytesIO

def pdf_photo():
    pdf_file = "transfer-receipt-13_706129645213422312.pdf"
    output_dir = "images"
    os.makedirs(output_dir, exist_ok=True)

    doc = fitz.open(pdf_file)

    for page_number in range(len(doc)):
        page = doc[page_number]
        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = f"page{page_number + 1}_img{img_index + 1}.{image_ext}"

            # 🔍 Работа с изображением через PIL
            file_io = BytesIO(image_bytes)
            image = Image.open(file_io)

            # 👉 Пример: уменьшить размер и сохранить копию
            resized = image.resize((300, 300))
            resized_path = os.path.join(output_dir, f"resized_{image_filename}")
            resized.save(resized_path)
            print(f"Сохранено уменьшенное изображение: {resized_path}")

            # 👉 Если хочешь что-то ещё — например, распознать текст или применить фильтр — добавляй тут

    print("Обработка завершена.")

#pdf_photo()