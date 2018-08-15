FROM mengnabai/bonjourai:v1.2
RUN apt-get update -y
# RUN apt-get install -y vim
# RUN apt-get install -y python3-pip
COPY . /data/app
WORKDIR /data/app
# RUN pip3 install -r requirements.txt
# ENTRYPOINT ["python3"]
# CMD ["weixin_app.py"]
