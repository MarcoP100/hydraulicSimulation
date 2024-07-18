FROM debian:12

# Imposta il frontend non interattivo per evitare richieste durante l'installazione dei pacchetti
ENV DEBIAN_FRONTEND=noninteractive

# Installa dipendenze e strumenti necessari
RUN apt-get update && \
    apt-get install -y ca-certificates curl gnupg

# Aggiungi la chiave GPG e il repository di OpenModelica
RUN curl -fsSL http://build.openmodelica.org/apt/openmodelica.asc | gpg --dearmor -o /usr/share/keyrings/openmodelica-keyring.gpg && \
    echo "deb [arch=arm64 signed-by=/usr/share/keyrings/openmodelica-keyring.gpg] https://build.openmodelica.org/apt $(cat /etc/os-release | grep "\(UBUNTU\\|DEBIAN\\|VERSION\)_CODENAME" | sort | cut -d= -f 2 | head -1) stable" | tee /etc/apt/sources.list.d/openmodelica.list

# Aggiorna i pacchetti e installa OpenModelica
RUN apt-get update && \
    apt-get install -y openmodelica \
    xfce4 \
    xfce4-goodies \
    tightvncserver \
    dbus-x11 \
    wget \
    apt-utils \
    nano \
    && apt-get clean

RUN apt-get update && \
    apt-get install -y sudo \
    git \
    autocutsel \
    openssh-server \
    && apt-get clean

# Genera le chiavi host SSH
RUN ssh-keygen -A

# Crea la directory per i file di configurazione SSH
RUN mkdir /var/run/sshd

# Crea un utente non privilegiato
RUN useradd -m -s /bin/bash vncuser && echo "vncuser:marco#" | chpasswd && adduser vncuser sudo

# Configura sudo per non richiedere password temporaneamente
RUN echo "vncuser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/temporary

# Copiare lo script di avvio nel contenitore
COPY start_vnc.sh /start_vnc.sh
RUN chmod +x /start_vnc.sh && chown vncuser:vncuser /start_vnc.sh
# Copia lo script di avvio nel container
COPY start_services.sh /start_services.sh
RUN chmod +x /start_services.sh

# Configurare VNC
RUN mkdir -p /home/vncuser/.vnc \
    && echo "marco123" | vncpasswd -f > /home/vncuser/.vnc/passwd \
    && chmod 600 /home/vncuser/.vnc/passwd \
    && echo "#!/bin/sh\n \
    autocutsel -fork\n \
    exec startxfce4" > /home/vncuser/.vnc/xstartup \
    && chmod +x /home/vncuser/.vnc/xstartup \
    && chown -R vncuser:vncuser /home/vncuser/.vnc

# Aggiungi comandi di debug per verificare i permessi e la proprietà
RUN ls -l /start_vnc.sh && \
    ls -l /home/vncuser/.vnc && \
    cat /home/vncuser/.vnc/xstartup


# Configura SSH per permettere l'accesso con chiave pubblica e disabilitare l'accesso root
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
RUN sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config

# Crea la directory .ssh per l'utente vncuser e imposta i permessi corretti
RUN mkdir -p /home/vncuser/.ssh && chown vncuser:vncuser /home/vncuser/.ssh && chmod 700 /home/vncuser/.ssh

# Copia la chiave pubblica nella directory .ssh del nuovo utente
COPY id_rsa_openmodelica.pub /home/vncuser/.ssh/authorized_keys
RUN chown vncuser:vncuser /home/vncuser/.ssh/authorized_keys && chmod 600 /home/vncuser/.ssh/authorized_keys

# Esponi la porta 22
EXPOSE 22
# Esporre la porta 5901
EXPOSE 5901

# Passa all'utente non privilegiato
USER vncuser

# Comando per avviare lo script di avvio
CMD ["/start_services.sh"]