#!/bin/sh

echo start write elastic > ./elasticbuild/setupelastic.log

docker run \
--net=host \
--env-file .env \
--rm -it \
-v ./elasticbuild/setupelastic.log:/opt/app/setupelastic.log:rw \
$(docker build -q elasticbuild)