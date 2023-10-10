#!/bin/bash

failed_namespaces=()
pod_data=()

# Get a list of failed pods in all namespaces
failed=$(kubectl get po -A | grep -iv 'running\|completed')

while read -r line; do
  namespace_name=$(echo "$line" | awk '{print $1}')
  pod_name=$(echo "$line" | awk '{print $2}')
  pod_status_value=$(echo "$line" | awk '{print $4}')
  pod_state_value=$(echo "$line" | awk '{print $3}')

  # Skip the "NAME" header
  if [ "$pod_name" != "NAME" ]; then
    # Append information to the arrays
    failed_namespaces+=("$namespace_name")
    pod_id="${pod_name}-${namespace_name}+1"

    # Get logs and escape double quotes
    logs=$(kubectl logs -n "$namespace_name" "$pod_name" 2>&1 | sed 's/"/\\"/g')

    # Create a JSON object for pod data
    pod_info="{\"namespace\":\"$namespace_name\",\"pod_id\":\"$pod_id\",\"pod_name\":\"$pod_name\",\"pod_status\":\"$pod_status_value\",\"pod_state\":\"$pod_state_value\",\"logs\":\"$logs\"}"

    pod_data+=("$pod_info")
  fi
done <<< "$failed"

# Construct the final JSON object
json_data="{\"pod_data\":["

for ((i = 0; i < ${#pod_data[@]}; i++)); do
  json_data+="${pod_data[i]}"
  if [ $i -lt $(( ${#pod_data[@]} - 1 )) ]; then
    json_data+=","
  fi
done
json_data+="]}"

# Save JSON data to a file
echo "$json_data" > output.json