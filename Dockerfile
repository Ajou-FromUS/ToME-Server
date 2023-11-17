FROM fastapi:origin
COPY ./src /server/fastapi
WORKDIR /server/fastapi/
RUN pip install -r requirements.txt
CMD ["uvicorn","main:app","--reload","--host","0.0.0.0","--workers","4"]