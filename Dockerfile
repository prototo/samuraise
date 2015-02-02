FROM base/arch

RUN pacman -Syy --noconfirm python python-pip
RUN pip install pyramid nltk waitress
RUN python -m nltk.downloader all
ADD summarise /summarise
WORKDIR /summarise
RUN python setup.py develop

CMD pserve development.ini --reload
