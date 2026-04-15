## Installare Redis su ultra.cc senza sudo

* wget https://download.redis.io/redis-stable.tar.gz

* tar xzf redis-stable.tar.gz

* cd redis-stable

* make

### Configura redis

- cd redis-stable
- nano redis.conf
    - verifica che sia presente la stringa "bind 127.0.0.1"
    - Cambia la porta da "port 6379" a "port 7000"
    - ctrl-o per salvare
    - ctrl-x per uscire da nano
- cd src
- [non lanciare redis senza specificare il file di configurazione]
- ./redis-server ../redis.conf --daemonize yes

#### Test Redis server

- ./redis-cli ping

#### Shutdown Redis server

Nel caso servisse chiudere redis

- ./redis-cli -p 7000 shutdown

### Configura tunnel ssh per raggiungere il backend dal tuo browser

ssh -L 7000:localhost:7000 -L 8000:localhost:8000 utente_tuo_server@ip_del_tuo_server -N

## Test veloce di connessione a Redis lato client

- nc 127.0.0.1 7000
- ping -> il server deve rispondere PONG

Ora puoi collegarti al bot attraverso il browser all'indirizzo 127.0.0.1:8000

### Configura memoria

- ```under construction```

---