const logoutbtn = document.querySelector('#logoutbtn')

logoutbtn.addEventListener('click', () => {
    sessionStorage.clear();
    window.location.href='/';
})

' JavaScript code to handle slot selection and saving availability '

// Wait until the whole HTML page (DOM) is fully loaded before running the script
document.addEventListener("DOMContentLoaded", () => {

  // Select all the slot buttons (each time slot button like 08:00–12:00)
  const slotButtons = document.querySelectorAll(".slot-btn");

  // Select the "Save" button at the bottom
  const saveBtn = document.getElementById("save-btn");

  // -----------------------------
  // 1️⃣ SLOT SELECTION TOGGLE LOGIC
  // -----------------------------
  // For each slot button, add a click event listener
  slotButtons.forEach(btn => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();  // Prevents form submission if button is inside a <form>

      // Toggle the "selected" class (adds it if missing, removes it if already there)
      // This is what makes the button turn green using CSS
      btn.classList.toggle("selected");
    });
  });

  // -----------------------------
  // 2️⃣ SAVE BUTTON LOGIC
  // -----------------------------
  saveBtn.addEventListener("click", async (e) => {
    e.preventDefault();  // Prevent default form submission behavior

    // Collect all buttons that have been selected (green)
    const selectedSlots = Array.from(slotButtons)
      .filter(btn => btn.classList.contains("selected"))  // only selected ones
      .map(btn => ({
        date: btn.dataset.date,  // extract date from "data-date" attribute
        slot: btn.dataset.slot   // extract slot time from "data-slot" attribute
      }));

    // If no slots are selected, show a message and stop
    if (selectedSlots.length === 0) {
      alert("No slots selected!");
      return;
    }

    // -----------------------------
    // 3️⃣ SEND DATA TO BACKEND
    // -----------------------------
    // We send the selected slots to Flask backend using the Fetch API
    // It sends data as JSON (not form data)
    const response = await fetch("/Doctor", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"  // Tell Flask it's JSON data
      },
      body: JSON.stringify({ slots: selectedSlots })  // Convert JS object to JSON string
    });

    // Wait for the server to reply, then convert it to JSON
    const data = await response.json();

    // -----------------------------
    // 4️⃣ SHOW FEEDBACK TO USER
    // -----------------------------
    // Show a popup message returned from Flask (like "Availability updated successfully!")
    alert(data.message);


  });
});



// Provide availability pop up 

document.addEventListener('DOMContentLoaded', () => {
  const provide_availability_btn = document.querySelector('#availability-btn');
  const doctor_availability_div = document.querySelector('.doctoravailability');

  if (provide_availability_btn && doctor_availability_div) {
    provide_availability_btn.addEventListener('click', () => {
      doctor_availability_div.style.display = 'flex';
    });
  } else {
    console.warn('Button or div not found');
  }
});

// Back button to close availability pop up

document.addEventListener('DOMContentLoaded', () => {
  const da_back_btn = document.querySelector('#da-back-btn');
  const doctor_availability_div = document.querySelector('.doctoravailability');

  if (da_back_btn && doctor_availability_div) {
    da_back_btn.addEventListener('click', () => {
      doctor_availability_div.style.display = 'none';
    });
  } else {
    console.warn('Button or div not found');
  }
});

//back button to close update patient history box

document.addEventListener('DOMContentLoaded', () => {
  const uph_back_btn = document.querySelector('#uph-back-btn');
  const update_patient_history_div = document.querySelector('.updatepatienthistory'); 
  if (uph_back_btn && update_patient_history_div) {
    uph_back_btn.addEventListener('click', () => {
      update_patient_history_div.style.display = 'none';
    });
  } else {
    console.warn('Button or div not found');
  }
});


// temp variables for storing patient and appointment ids

let currentPatientId = null;
let currentAppointmentId = null;

// update button to pop up update patient history box
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.UA-patient-history-update-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            // Get data from button attributes
            currentPatientId = this.getAttribute('data-patient_id');
            const patientName = this.getAttribute('data-patient_name');
            const department = this.getAttribute('data-department_name');
            currentAppointmentId = this.getAttribute('data-appointment_id');

            // Show the Update Patient History section if it's hidden
            document.querySelector('.updatepatienthistory').style.display = 'flex';
            
            // Fill form fields
            document.getElementById('uph-patient_name').innerText = "Patient Name : " +  patientName;
            document.getElementById('uph-department').innerText = "Department : "  +  department;
            
        });
    });
  });

// Updating Patient History in DB

// These store the values temporarily between button click and form submission


document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('.uph-form').addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent default form submission

        // Collect form data
        const appointmentId = currentAppointmentId;
        const patientId = currentPatientId;
        const visitType = document.getElementById('visittype')?.value || '';
        const testdone = document.getElementById('testdone')?.value || '';
        const diagnosis = document.getElementById('diagnosis')?.value || '';
        const prescription = document.getElementById('prescription')?.value || '';
        const notes = document.getElementById('notes')?.value || '';

        // Prepare data to send
        const formData = {
            appointment_id: appointmentId,
            patient_id: patientId,
            
        };

        if (visitType) formData.visit_type = visitType;
        if (testdone) formData.test_done = testdone;
        if (diagnosis) formData.diagnosis = diagnosis;
        if (prescription) formData.prescription = prescription;
        if (notes) formData.notes = notes;

        console.log('Form Data to be sent:', formData);
        

        // Send data to backend using Fetch API
        const response = await fetch('/save_treatment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        // handle responses
        const data = await response.json();
        if (data.success) {
            alert('Patient history updated successfully!');
            // Optionally, close the update form
            document.querySelector('.updatepatienthistory').style.display = 'none';
        } else {
            alert('Error updating patient history: ' + data.error);
        }

    });
});  


// Mariking appointments as completed

document.addEventListener('DOMContentLoaded', () => {

    const mark_as_completed_buttons = document.querySelectorAll('.UA-mark_as_complete-btn');
    mark_as_completed_buttons.forEach(btn => {
      btn.addEventListener('click', async function() {
        const appointmentId = this.getAttribute('data-appointment_id');
        const response = await fetch('/mark_appointment_complete', {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ appointment_id: appointmentId })
        });

        const data = await response.json();
        if (data.success) {
          alert('Appointment marked as complete!');
        } else {
          alert('Error marking appointment as complete: ' + data.error);
        }
      });
    });
});



// Patient history div  pop off

document.addEventListener('DOMContentLoaded', () => {
  const patient_history_back_btn = document.querySelector('#PH-back-btn');

  patient_history_back_btn.addEventListener('click', () => {
    const patient_history_div = document.querySelector('.patienthistory');
    patient_history_div.style.display = 'none';
  });

});


// patinet history div pop up 

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.AP-patient-history-view-btn').forEach(btn => {
  btn.addEventListener('click', function() {
    const patientId = btn.dataset.patient_id;
    const doctorId = btn.dataset.doctor_id;

    console.log('Fetching history for Patient ID:', patientId, 'Doctor ID:', doctorId);

    fetch(`/get-patient-history/${patientId}/${doctorId}`) // This route should return JSON!
      .then(response => response.json())
      .then(data => {
        // Update patient info headers
        document.querySelector('#doctorname').textContent = "DR. " + data.doctor.first_name;
        document.querySelector('#patientname').textContent = "MR. " + data.patient.first_name;
        document.querySelector('#departmentname').textContent = data.department.department_name;

        // Fill the table body
        const tbody = document.querySelector('#PH-table-body');
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
});