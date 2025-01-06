document.getElementById('apply-form').addEventListener('submit', function(e) {
  e.preventDefault();
  apply();
});

function validateApplyForm() {
  const studentId = document.getElementById('student_id').value;
  if (!studentId) {
      alert('Please fill in your student ID.');
      return false;
  }
  return true;
}

function apply() {
  if (!validateApplyForm()) return;

  const studentId = document.getElementById('student_id').value;
  const additionalFields = document.getElementById('additional-fields').elements;
  let studentInfo = {};

  for (let field of additionalFields) {
      if (field.value) {
          studentInfo[field.name] = field.value;
      }
  }

  fetch('/apply', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          student_id: studentId,
          event_id: eventId,
          student_info: studentInfo
      })
  })
  .then(response => response.json())
  .then(data => {
      alert(data.status);
  });
}

// function apply() {
//     const eventId = document.getElementById('event_id').value;
//     const studentId = document.getElementById('student_id').value;

//     fetch('/apply', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({
//             event_id: eventId,
//             student_id: studentId,
//             student_info: {
//                 // Add additional fields here
//             }
//         })
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.status === 'Application received') {
//             alert('Application submitted successfully.');
//         } else {
//             alert('Failed to submit application.');
//         }
//     })
//     .catch(error => {
//         console.error('Error:', error);
//         alert('[_{{{CITATION{{{_1{](https://github.com/alfredofloresf/assignment2/tree/193a668d505740f3508750ec00cdb6f2ac774a31/app.py)[_{{{CITATION{{{_2{](https://github.com/cnjllin/actual-16-homework/tree/c4937af205dd7cee3ee39223f8b9271059e72d7e/lesson6%2Fyangjianjiang%2Fflask_web.py)[_{{{CITATION{{{_3{](https://github.com/slawek367/CurrencyExchange/tree/e4d75afdb03018a59c498843212c4d5fc4da3211/FlaskApp.py)[_{{{CITATION{{{_4{](https://github.com/yupeng0921/aws_customer_life_cycle/tree/127777a26574db2c7e86c4577ec8be0a4a140a5c/src%2Fserver.py)[_{{{CITATION{{{_5{](https://github.com/setornando/blogz/tree/471b03e1772017a5682aac8f4f29a2aae7aa1c2b/main.py)[_{{{CITATION{{{_6{](https://github.com/TheClaireBear/blogz/tree/b3f4cec9038ec598d00e0ed44e2ad5df65edc5b1/main.py)[_{{{CITATION{{{_7{](https://github.com/mahoney777/CMUI/tree/7b2db5bc9e1487b5f91db4dfb677ba5a8fa330a8/KSApp%2Fviews.py)
