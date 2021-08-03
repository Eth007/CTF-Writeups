FROM redpwn/jail

COPY --from=ubuntu / /srv
COPY dist/*_admin.zip /srv/app/admin.zip
RUN unzip /srv/app/admin.zip -d /srv/app/
RUN rm /srv/app/admin.zip
RUN mv /srv/app/inkaphobia /srv/app/run

ENV JAIL_TIME 120
ENV JAIL_CONNS_PER_IP 1
ENV JAIL_MEM 20M
