
#!/bin/bash
set -e
if [ ! -z "$EXTRA_PIP_PACKAGES" ]; then
  echo "+pip install $EXTRA_PIP_PACKAGES"
  pip install $EXTRA_PIP_PACKAGES
fi
if [ -z "$*" ]; then
  exec bash --login
else
  exec "$@"
fi