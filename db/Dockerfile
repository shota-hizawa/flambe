FROM mysql:5.7

ADD ./initdb.d /docker-entrypoint-initdb.d

COPY ./custom-config.cnf /etc/mysql/conf.d/custom-config.cnf
