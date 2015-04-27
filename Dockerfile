FROM base/arch


EXPOSE 6543
ADD summarise /summarise
WORKDIR /summarise

RUN pacman -Syy --noconfirm python python-pip
RUN pip install pyramid nltk waitress
RUN python -m nltk.downloader book
RUN python setup.py develop

CMD pserve development.ini --reload
