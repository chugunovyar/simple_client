FROM python:3.11
LABEL authors="chugunovyar@gmail.com"

COPY . code/
RUN pip install -r code/requirements.txt
WORKDIR code/
CMD ["fastapi", "run", "main.py", "--port", "8000"]