sudo apt update && sudo apt install -y build-essential git libexpat1-dev libssl-dev zlib1g-dev \
libncurses5-dev libbz2-dev liblzma-dev \
libsqlite3-dev libffi-dev tcl-dev linux-headers-generic libgdbm-dev \
libreadline-dev tk tk-dev

curl https://pyenv.run | bash

Adicionar no .~/.zshrc
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

eval "$(pyenv virtualenv-init -)"
