# 🧾 Django Inventory Management System

A complete **Inventory Management System** built with **Django**.  
It manages **Products, Suppliers, Purchases, Stock, and Payments** efficiently —  
ideal for small to medium-sized businesses.

---

## 🚀 Features

✅ Product management (with SKU, brand, color, unit)  
✅ Supplier management  
✅ Purchase & payment entry (cash, bank, due, mixed)  
✅ Auto stock update after purchase  
✅ Product purchase price history tracking  
✅ Serial & IMEI number support per item  
✅ Manual invoice number + auto lot number  
✅ Django admin customization  
✅ Responsive and simple UI  

---

## 🛠️ Tech Stack

| Component | Technology |
|------------|-------------|
| Backend | Django (Python) |
| Database | SQLite (default) |
| Frontend | HTML, CSS, Bootstrap |
| Version Control | Git + GitHub |

---

## ⚙️ Installation Guide

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/engrrasel/inventory_management.git
cd inventory_management


2️⃣ Create Virtual Environment
python -m venv env

3️⃣ Activate the Environment
🔹 For Windows:
env\Scripts\activate

🔹 For Linux/Mac:
source env/bin/activate

4️⃣ Install Dependencies
pip install -r requirements.txt

5️⃣ Run Database Migrations
python manage.py makemigrations
python manage.py migrate

6️⃣ Create Superuser
python manage.py createsuperuser

7️⃣ Run the Server
python manage.py runserver


Then open your browser and go to 👉
http://127.0.0.1:8000/admin/

📦 Folder Structure
inventory_management/
│
├── app_product/           # Product, Brand, Unit management
├── app_purchase/          # Purchase and payment management
├── app_stock/             # Stock tracking
├── templates/             # HTML templates
├── static/                # CSS, JS, images
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md

🧑‍💻 Author

Name: Rasel Mia
📧 Email: eng.raselmiah@gmail.com
]
🌐 GitHub: https://github.com/engrrasel

📜 License

This project is open-source and available under the MIT License.

⭐ If you like this project, don’t forget to give it a star on GitHub!