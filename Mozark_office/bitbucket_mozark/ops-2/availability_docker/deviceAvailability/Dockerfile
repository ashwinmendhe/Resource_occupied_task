# DockerFile, Image, Container
FROM python
ADD device_avilability2_6_7.py .
ADD main.py .
ADD requirements.txt .
ADD .env .
# RUN chmod +x env.sh
RUN pip install -r requirements.txt
CMD ["python3", "./main2_6_7.py"]
# ENTRYPOINT ["./env.sh"]