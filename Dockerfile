FROM python:3.8
#RUN  mkdir /urldetective
RUN  pip install flask requests pickle5  beautifulsoup4  regex numpy pandas sklearn
RUN  pip install fuzzywuzzy
RUN  pip install python-Levenshtein

COPY data /data
COPY templates templates
ADD  app.py app.py
ADD  deepchecks.py deepchecks.py
ADD  preprocessing.py preprocessing.py
ADD  RFCmodel.pkl RFCmodel.pkl
#docker run -p 5000:5000 urldetective
CMD  ["python","./app.py"]