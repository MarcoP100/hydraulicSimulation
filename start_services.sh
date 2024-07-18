#!/bin/bash

# Aggiungi messaggi di debug
echo "Avvio del server SSH..."
sudo /usr/sbin/sshd
if [ $? -eq 0 ]; then
  echo "Server SSH avviato con successo"
else
  echo "Errore nell'avvio del server SSH"
  exit 1
fi

echo "avvio VNC..."
#su - vncuser -c "/start_vnc.sh"
/start_vnc.sh
if [ $? -eq 0 ]; then
  echo "Server VNC avviato con successo"
else
  echo "Errore nell'avvio del server VNC"
  exit 1
fi

# Ripristina la richiesta di password per sudo
echo "Ripristino della richiesta di password per sudo..." | tee -a /var/log/start_services.log
sudo rm /etc/sudoers.d/temporary
if [ $? -eq 0 ]; then
  echo "Configurazione sudo ripristinata con successo" | tee -a /var/log/start_services.log
else
  echo "Errore nel ripristino della configurazione sudo" | tee -a /var/log/start_services.log
  exit 1
fi

# Mantieni il contenitore in esecuzione
tail -f /dev/null
