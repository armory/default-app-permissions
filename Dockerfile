FROM python:3.6

COPY ./ /default_app_permisions

RUN pip install /default_app_permisions/

ENTRYPOINT ["/usr/local/bin/default-app-permissions"]
