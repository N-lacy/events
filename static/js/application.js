function apply() {
  const eventId = document.getElementById('event_id').value;
  const studentId = document.getElementById('student_id').value;
  const studentName = document.getElementById('student_name').value;
  const studentPassportNumber = document.getElementById('student_passport_number').value;
  const studentPhoneNumber = document.getElementById('student_phone_number').value;

  fetch('/apply', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          event_id: eventId,
          student_id: studentId,
          student_info: {
              name: studentName,
              passport_number: studentPassportNumber,
              phone_number: studentPhoneNumber
          }
      })
  })
  .then(response => response.json())
  .then(data => {
      if (data.status === 'Application received') {
          alert('Application submitted successfully.');
      } else {
          alert('Failed to submit application.');
      }
  })
  .catch(error => {
      console.error('Error:', error);
      alert('An error occurred. Please try again.');
  });
}
