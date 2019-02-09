FROM google/cloud-sdk

RUN apt-get update && apt-get install python3-pip -y

RUN pip3 install ansible openshift

RUN pip install ansible openshift

RUN apt-get install -y  \
     apt-transport-https \
     ca-certificates \
     curl \
     gnupg2 \
     software-properties-common

RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -

RUN add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   stable"

RUN apt-get update && apt-get install docker-ce -y
