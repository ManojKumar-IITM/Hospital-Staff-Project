document.querySelectorAll('.patienthistorybutton').forEach(btn => {
  btn.addEventListener('click', function() {
    const patientId = btn.dataset.patientId;
    const doctorId = btn.dataset.doctorId;

    fetch(`/get-patient-history/${patientId}/${doctorId}`) // This route should return JSON!
      .then(response => response.json())
      .then(data => {
        // Update patient info headers
        document.querySelector('#doctorname').textContent = data.doctor.first_name;
        document.querySelector('#patientname').textContent = data.patient.first_name;
        document.querySelector('#departmentname').textContent = data.department.department_name;

        // Fill the table body
        const tbody = document.querySelector('#patienthistorytable');
        tbody.innerHTML = ""; // Clear old data

        
        data.patient_history.forEach((row, idx) => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td>${idx+1}</td>
            <td>${row.visittype}</td>
            <td>${row.testdone}</td>
            <td>${row.diagnosis}</td>
            <td>${row.prescription}</td>
            <td>${row.notes}</td>
          `;
          tbody.appendChild(tr);
        });
      });
    document.querySelector('.patienthistory').style.display = 'flex';
    
  });
});



document.querySelector('#back-btn').addEventListener('click', function() {
  document.querySelector('.patienthistory').style.display = 'none';
});


const logoutbtn= document.querySelector('#logoutbutton')

logoutbtn.addEventListener('click', function(){
  sessionStorage.clear();
  window.location.href='/';
})
