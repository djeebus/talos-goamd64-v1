test VERSION:
  #!/usr/bin/env bash

  event_file=$(mktemp)
  cat << EOF >> $event_file
  {"action":"workflow_dispatch", "inputs": {"version":"{{ VERSION }}"} }
  EOF
  act --job build-release --eventpath $event_file
