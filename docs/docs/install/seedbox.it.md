# Installazione su seedbox ultra.cc

Ultra.cc non permette l'uso di `sudo`, quindi serve qualche passaggio in più rispetto a un Linux normale.

Il bot richiede Python con versione minima 3.10 (consigliata: fino alla 3.12 — le versioni più recenti risultano ancora troppo nuove per alcune librerie).

Su ultra.cc è preinstallato **pyenv**, che useremo per installare Python. Unico problema: pyenv non installa sqlite3, che il bot usa come cache per screenshot e ricerche sul tracker. Va quindi compilato sqlite3 (un paio di comandi) e poi installato Python 3.12.

## 1. Installare sqlite3

Senza `sudo` dobbiamo compilare. Vai nella home:

```bash
cd ~
```

Scarica il pacchetto:

```bash
wget https://sqlite.org/2026/sqlite-autoconf-3510300.tar.gz
```

Scompattalo:

```bash
tar xvf sqlite-autoconf-3510300.tar.gz
```

Entra nella cartella ottenuta:

```bash
cd sqlite-autoconf-3510300
```

Lancia questi tre comandi uno dietro l'altro:

```bash
./configure --prefix=$HOME/sqlite
make
make install
```

Imposta le variabili d'ambiente **solo per questa sessione** — copia e incolla nel terminale SSH:

```bash
export PATH=$HOME/sqlite/bin:$PATH
export LDFLAGS="-L$HOME/sqlite/lib"
export CPPFLAGS="-I$HOME/sqlite/include"
export PKG_CONFIG_PATH="$HOME/sqlite/lib/pkgconfig"
export PYTHON_CONFIGURE_OPTS="--enable-loadable-sqlite-extensions"
export LD_LIBRARY_PATH=$HOME/sqlite/lib:$LD_LIBRARY_PATH
```

## 2. Installare Python 3.12

```bash
pyenv install -f 3.12.0
```

Imposta Python 3.12 come versione di default:

```bash
pyenv global 3.12.0
```

## 3. Installare e testare il bot

```bash
pip install unit3dup
```

Lancia il bot come primo test:

```bash
unit3dup
```

![avvio](../images/unit3dup.png)

I messaggi in rosso ti avvertono che non hai ancora configurato il bot: prosegui con la [Configurazione minima](../config/intro.md).

## Se pyenv non è presente

Lancia nel terminale:

```bash
curl -fsSL https://pyenv.run | bash
```

Istruzioni complete sul [GitHub di pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#linuxunix).
