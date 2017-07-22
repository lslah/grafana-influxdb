FROM library/python

RUN pip install requests psutil


RUN useradd -ms /bin/bash py
COPY mem.py /home/py/mem.py
RUN chown py:py /home/py/mem.py
USER py
