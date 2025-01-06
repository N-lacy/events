#!/bin/bash

# Function to generate random string
generate_random_string() {
  cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 10 | head -n 1
}

# Function to generate random date
generate_random_date() {
  date -d "$((RANDOM%30+1)) days" +"%Y-%m-%d"
}

# Create events
for i in {1..5}
do
  event_name="Event_$(generate_random_string)"
  required_fields="name,passport_number,phone_number"
  mandatory_students="$(generate_random_string),$(generate_random_string)"
  event_date=$(generate_random_date)
  num_students=$((RANDOM%20+5))

  response=$(curl -s -X POST http://localhost:5000/create_event -H "Content-Type: application/json" -d '{
    "event_name": "'${event_name}'",
    "required_fields": "'${required_fields}'",
    "mandatory_students": "'${mandatory_students}'",
    "event_date": "'${event_date}'",
    "num_students": '${num_students}'
  }')

  # Print the full response
  echo "Full response: ${response}"

  # Extract the event ID from the response using jq
  qr_code_url=$(echo $response | jq -r '.qr_code_url')
  event_id=$(basename $qr_code_url | sed 's/_qr.png//')

  echo "Created event with ID: ${event_id}"

  # Apply students to the event
  for j in {1..40}
  do
    student_id=$(generate_random_string)
    student_name="Student_${student_id}"
    passport_number="P$(generate_random_string)"
    phone_number="$(generate_random_string)"

    curl -s -X POST http://localhost:5000/apply -H "Content-Type: application/json" -d '{
      "student_id": "'${student_id}'",
      "event_id": "'${event_id}'",
      "student_info": {
        "name": "'${student_name}'",
        "passport_number": "'${passport_number}'",
        "phone_number": "'${phone_number}'"
      }
    }'
  done
done

echo "Simulated applications added successfully!"
