FROM python:3.8
# set work directory
WORKDIR /tg_bot/
# copy project
COPY . /tg_bot/
# install dependencies
RUN pip install -r requirements.txt
# run app
CMD ["python", "main.py"]