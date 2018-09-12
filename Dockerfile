FROM python:3.6-slim
RUN useradd -m appuser
WORKDIR /home/appuser
COPY app/ ./app/
COPY app_config.py requirments.txt run_gunicorn.sh ./

RUN pip install --no-cache-dir -r requirments.txt
RUN chmod +x run_gunicorn.sh
RUN chown -R appuser:appuser ./
USER appuser

# check which port is used in run_gunicorn.sh file
EXPOSE 7000
ENTRYPOINT ["./run_gunicorn.sh"]
