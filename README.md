# Django E-Commerce Project Deployment Guide for PythonAnywhere

## Prerequisites
- PythonAnywhere Account (Free Tier)
- GitHub Repository
- Basic understanding of Django and Python

## Deployment Steps

### 1. PythonAnywhere Setup
1. Create a PythonAnywhere account (https://www.pythonanywhere.com/)
2. Open a Bash console

### 2. Clone Repository
```bash
git clone https://github.com/ahmedElsayedHussien/ExEcommerce.git
cd ExEcommerce
```

### 3. Create Virtual Environment
```bash
mkvirtualenv --python=/usr/bin/python3.8 myenv
source myenv/bin/activate
pip install -r requirements.txt
```

### 4. Database Configuration
- Go to PythonAnywhere Web tab
- Create a MySQL database
- Update `settings.py` with:
  - Database Name: `yourusername$ecommerce`
  - User: Your PythonAnywhere username
  - Host: `yourusername.mysql.pythonanywhere-services.com`

### 5. Collect Static Files
```bash
python manage.py collectstatic
```

### 6. Run Migrations
```bash
python manage.py migrate
```

### 7. Web App Configuration
- Go to PythonAnywhere Web tab
- Add a new web app
- Choose Manual configuration
- Python version: Python 3.8
- Virtualenv path: `/home/yourusername/.virtualenvs/myenv`
- Code directory: `/home/yourusername/ExEcommerce`
- WSGI configuration file: `/home/yourusername/ExEcommerce/wsgi.py`

### 8. Environment Variables
Set these in PythonAnywhere Web tab > Web app > Environment variables:
- `SECRET_KEY`: Your Django secret key
- `DEBUG`: `False`
- `ALLOWED_HOSTS`: Your PythonAnywhere domain

### Troubleshooting
- Check PythonAnywhere error logs
- Ensure all dependencies are installed
- Verify database connection
- Check file permissions

### Project Structure
```
ExEcommerce/
│
├── ecommerce_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── store/
│   ├── models.py
│   ├── views.py
│   └── ...
│
├── templates/
│   └── ...
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/
│   └── ...
│
├── requirements.txt
└── manage.py
```

## Additional Notes
- Keep your secret key confidential
- Regularly update dependencies
- Use environment-specific settings

## License
[Specify your project's license]

## Contact
Ahmed Elsayed - ahbezo4@gmail.com
