FROM python:3.9

RUN pip install dash_html_components
RUN pip install dash
RUN pip install dash_core_components
RUN pip install dash_html_components
RUN pip install dash_bootstrap_components
RUN pip install pandas
RUN pip install numpy
RUN pip install scipy
RUN pip install plotly
RUN pip install networkx
RUN pip install dash_cytoscape
RUN pip install anndata

RUN mkdir /home/app/
COPY . /home/app/
WORKDIR /home/app/
EXPOSE 8050

ENTRYPOINT ["python", "index_whole.py"]