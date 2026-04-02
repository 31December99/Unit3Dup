# Nel caso pyenv non fosse già installato sul vostro sistema operativo
___


## Linux

Copia l'intero blocco e incollalo nel terminale. Digita la password

```sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev ```

![Descrizione](images/pythonenv01_debian.png)
Lancia curl https://pyenv.run | bash

Copia e incolla nel file ~/.bashrc alla fine del file

```
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
```

Salva e chiudi

lancia source ~/.bashrc



