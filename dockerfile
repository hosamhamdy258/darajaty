FROM python:3.10.13-slim

# Set environment variables
# ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
COPY core_packages.txt .

RUN pip install wheel
RUN pip install --no-cache-dir -r core_packages.txt

COPY . .

EXPOSE 8000

# RUN python manage.py collectstatic --noinput

# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
