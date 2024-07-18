#!/bin/bash
echo "Avvio del server VNC..."

# Imposta le variabili d'ambiente
export USER=vncuser
export HOME=/home/vncuser
export DISPLAY=:1

# Verifica delle variabili d'ambiente
echo "DISPLAY: $DISPLAY"
echo "USER: $USER"
echo "HOME: $HOME"

# Crea il file .Xauthority
touch $HOME/.Xauthority

# Verifica se il server VNC è già in esecuzione
echo "Verifica se il server VNC è già in esecuzione..."
if pgrep -x "Xtightvnc" > /dev/null; then
    echo "Il server VNC è già in esecuzione."
else
    echo "Il server VNC non è in esecuzione. Procedo con l'avvio..."

     # Debug: Mostra i file di lock
    echo "Contenuto della directory /tmp:"
    ls -la /tmp

    # Rimuovi il file di lock se esiste
    if [ -f /tmp/.X1-lock ]; then
        echo "Rimuovo /tmp/.X1-lock"
        sudo rm -f /tmp/.X1-lock
        echo "/tmp/.X1-lock rimosso."
    else
        echo "/tmp/.X1-lock non trovato."
    fi

    if [ -f /tmp/.X11-unix/X1 ]; then
        echo "Rimuovo /tmp/.X11-unix/X1"
        sudo rm -f /tmp/.X11-unix/X1
        echo "/tmp/.X11-unix/X1 rimosso."
    else
        echo "/tmp/.X11-unix/X1 non trovato."
    fi

    # Debug: Mostra di nuovo i file di lock
    echo "Contenuto della directory /tmp dopo la rimozione:"
    ls -la /tmp

    # Avvio del server VNC
    echo "Avvio del server VNC..."
    vncserver -geometry 1920x1080 -depth 24 $DISPLAY
    sleep 2
fi

# Verifica se il server VNC è in esecuzione
#ps aux | grep vnc

# Mantieni il contenitore in esecuzione
#tail -f /dev/null
