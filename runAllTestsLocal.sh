#!/usr/bin/bash
wget -qO /dev/null 'http://127.0.0.1:8000' || {
  echo "Webserver down"
  # another mailer example
#  sendemail -s mailserverip -f 'from@localhost' -t 'user@localhost' -u 'Webserver down' -m 'The webserver is down'
}
pytest tests
