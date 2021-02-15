FROM continuumio/miniconda3

WORKDIR /app

COPY environment.yml .
RUN conda env create -f environment.yml

COPY . .

CMD /opt/conda/envs/commentsearch/bin/python -m commentsearch
