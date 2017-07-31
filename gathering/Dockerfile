FROM library/python

RUN pip install requests psutil

ENV TINI_VERSION v0.15.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

RUN useradd -ms /bin/bash py
COPY mem.py /home/py/mem.py
RUN chown py:py /home/py/mem.py
USER py

ENTRYPOINT ["/tini", "--"]

CMD ["python", "/home/py/mem.py"]
