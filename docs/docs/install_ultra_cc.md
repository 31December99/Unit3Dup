# Installa Unit3dUp su seedbox ultra.cc
----

## Ultra.cc non permette l'uso di Sudo

Il bot richiede python con versione minima 3.10 mentre in questo momento su ultra.cc python è alla versione 3.9.

Utilizziamo **pyenv preinstallato su ultra.cc**. Unico problema pyenv non installa sqlite3.

Sqlite3 viene utilizzato dal bot come cache per screenshot e ricerche su tracker.

Occorre quindi installare sqlite3 (un paio di comandi) e poi python 3.10

---

### Installare sqlite3

Per installare sqlite3 non possiamo utilizzare sudo quindi dobbiamo compilare

Va in home

- ```cd ~```

Scarica il pacchetto con

- ```wget https://sqlite.org/2026/sqlite-autoconf-3510300.tar.gz```

Scompatta il pacchetto

- ```tar xvf sqlite-autoconf-3510300.tar.gz```

Entra nella cartella che hai ottenuto scompattando il tuo pacchetto

```cd sqlite-autoconf-3510300```

Lancia questi tre comandi uno dietro l'altro

```./configure --prefix=$HOME/sqlite```

```make```

```make install```

Imposta le variabili ambiente solo per questa sessione

Copia e incolla nel terminale 'ssh'

```
export PATH=$HOME/sqlite/bin:$PATH
export LDFLAGS="-L$HOME/sqlite/lib"
export CPPFLAGS="-I$HOME/sqlite/include"
export PKG_CONFIG_PATH="$HOME/sqlite/lib/pkgconfig"
export PYTHON_CONFIGURE_OPTS="--enable-loadable-sqlite-extensions"
```

### Installare python 3.10

Installa 

```pyenv install -f 3.10.0```

Setta python 3.10 come versione di sistema di default

```pyenv global 3.10.0```


Se hai già installato Unit3Dup, lancia il bot come primo test

```Unit3Dup```

![avvio](/images/unit3dup.png)

I messaggi in rosso ti avvertono che non hai ancora configurato il tuo bot [Configurazione minima](config.md)


### Se su ultra.cc non esiste pyenv

Lancia nel terminale

```curl -fsSL https://pyenv.run | bash```

[Dal loro github](https://github.com/pyenv/pyenv?tab=readme-ov-file#linuxunix)