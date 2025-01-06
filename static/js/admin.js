function validateForm() {
  const eventName = document.getElementById('event_name').value;
  const requiredFields = document.getElementById('required_fields').value;
  const eventDate = document.getElementById('event_date').value;
  const numStudents = document.getElementById('num_students').value;

  if (!eventName || !requiredFields || !eventDate || !numStudents) {
      alert('Please fill in all required fields.');
      return false;
  }
  return true;
}

function createEvent() {
  if (!validateForm()) return;

  const eventName = document.getElementById('event_name').value;
  const requiredFields = document.getElementById('required_fields').value.split(',');
  const mandatoryStudents = document.getElementById('mandatory_students').value.split(',');
  const eventDate = document.getElementById('event_date').value;
  const numStudents = document.getElementById('num_students').value;

  fetch('/create_event', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          event_name: eventName,
          required_fields: requiredFields,
          mandatory_students: mandatoryStudents,
          event_date: eventDate,
          num_students: numStudents
      })
  })
  .then(response => response.json())
  .then(data => {
      if (data.status === 'Event created') {
          document.getElementById('qr_code_section').style.display = 'block';
          document.getElementById('qr_code_image').src = data.qr_code_url;
          document.getElementById('qr_code_download').href = data.qr_code_url;
      } else {
          alert('Failed to create event');
      }
  })
  .catch(error => {
      console.error('Error:', error);
      alert('An error occurred. Please try again.');
  });
}

document.getElementById('create-event-form').addEventListener('submit', function(e) {
  e.preventDefault();
  createEvent();
});
