FROM python:3.8
# set work directory
WORKDIR /bot/
# copy project
COPY . /bot/
# install dependencies
RUN pip install -r requirements.txt
RUN pip install moralis
RUN pip install --upgrade aiogram pydantic typing_extensions
# run app
CMD ["python", "main.py"]