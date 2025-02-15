FROM fedora:latest

RUN dnf install -y openssh-server

RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#AllowTcpForwarding yes/AllowTcpForwarding yes/' /etc/ssh/sshd_config

RUN ssh-keygen -A

RUN echo "root:foobar" | chpasswd

# TODO: expose only on an isolated docker network to avoid conflicts?
#       Think about how extension would communicate
EXPOSE 5671
CMD ["/usr/sbin/sshd", "-D", "-p", "5671"]