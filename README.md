# Inventario GUI – Tkinter + SQLite  
Sistema de inventario profesional con interfaz gráfica y base de datos integrada.

## 🚀 Características
- CRUD completo (Create, Read, Update, Delete)
- Interfaz profesional con Tkinter + ttk.Treeview
- Arquitectura modular y escalable
- Base de datos SQLite persistente
- Instalación editable: `pip install -e .`
- Backend y GUI totalmente desacoplados

---

## 📂 Estructura del Proyecto

inventario_gui/
├── src/inventario_gui/
│ ├── app.py # Lógica de base de datos y CRUD
│ ├── gui.py # Interfaz Tkinter
│ └── init.py
├── pyproject.toml
├── requirements.txt
├── README.md
└── .gitignore

---

## 🛠️ Instalación

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .

----

▶️ Ejecutar la aplicación

python -m inventario_gui.gui

----

🗃️ Base de datos

La aplicación crea automáticamente inventario.db si no existe.

----

👤 Autor

Juan Sebastian Cristal

📄 Licencia

MIT License


----

# 🧱 **7. Subir cambios**

Cada vez que modifiques algo:


git add .
git commit -m "Added README and gitignore"
git push



