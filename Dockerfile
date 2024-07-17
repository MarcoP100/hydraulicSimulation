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
    autocutsel   

# Crea un utente non privilegiato
RUN useradd -m -s /bin/bash vncuser && echo "vncuser:marco#" | chpasswd && adduser vncuser sudo

# Copiare lo script di avvio nel contenitore
COPY start_vnc.sh /start_vnc.sh
RUN chmod +x /start_vnc.sh && chown vncuser:vncuser /start_vnc.sh

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

# Passa all'utente non privilegiato
USER vncuser

# Esporre la porta 5901
EXPOSE 5901

# Comando per avviare lo script di avvio
CMD ["/start_vnc.sh"]