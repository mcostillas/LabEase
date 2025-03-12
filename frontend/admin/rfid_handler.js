// RFID Handler for LabEase Log Book
document.addEventListener('DOMContentLoaded', function() {
    // Focus the RFID input on page load
    const rfidInput = document.getElementById('rfid-input');
    if (rfidInput) {
        rfidInput.focus();
    }

    // Dummy database of RFID cards
    const rfidDatabase = {
        "14230206": {
            id: "14230206",
            name: "Prof. Marc Costillas",
            department: "CCS",
            subject: "Mobile Application Development",
            section: "BSIT-3A",
            photoUrl: "../images/Marc.jpeg",
            status: "out" // can be "in" or "out"
        },
        "01641066": {
            id: "01641066",
            name: "Prof. Chloe Crausos",
            department: "Information Technology",
            subject: "Web Applications Development 2",
            section: "BSIT-2A",
            photoUrl: "../assets/profile-placeholder.jpg",
            status: "out"
        },
        "0087654321": {
            id: "0087654321",
            name: "Prof. Emily Johnson",
            department: "Computer Engineering",
            subject: "Data Structures and Algorithms",
            section: "BSCE-3B",
            photoUrl: "../assets/profile-placeholder.jpg",
            status: "out"
        }
    };

    // Get current date and time
    function getCurrentDateTime() {
        const now = new Date();
        const date = now.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        });
        const time = now.toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit',
            hour12: true 
        });
        return { date, time };
    }

    // Process RFID scan
    function processRfidScan(rfidId) {
        if (rfidDatabase[rfidId]) {
            const instructor = rfidDatabase[rfidId];
            showModal(instructor);
        } else {
            showNotification('RFID card not recognized. Please try again.', 'error');
        }
    }

    // Show modal with instructor information
    function showModal(instructor) {
        const modal = document.getElementById('rfid-modal');
        const modalName = document.getElementById('modal-name');
        const modalDepartment = document.getElementById('modal-department');
        const modalSubject = document.getElementById('modal-subject');
        const modalSection = document.getElementById('modal-section');
        const modalRfidId = document.getElementById('modal-rfid-id');
        const modalPhoto = document.getElementById('modal-photo');
        const modalAction = document.getElementById('modal-action');
        const confirmBtn = document.getElementById('confirm-action');

        // Set modal content
        modalName.textContent = instructor.name;
        modalDepartment.textContent = instructor.department;
        modalSubject.textContent = instructor.subject;
        modalSection.textContent = instructor.section;
        modalRfidId.textContent = instructor.id;
        modalPhoto.src = instructor.photoUrl || '../assets/profile-placeholder.jpg';

        // Determine action (time in or time out)
        const action = instructor.status === 'out' ? 'Time In' : 'Time Out';
        const actionIcon = instructor.status === 'out' 
            ? '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-right: 8px; vertical-align: -5px;"><path d="M11 16L7 12M7 12L11 8M7 12L21 12M16 16V17C16 18.6569 14.6569 20 13 20H6C4.34315 20 3 18.6569 3 17V7C3 5.34315 4.34315 4 6 4H13C14.6569 4 16 5.34315 16 7V8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
            : '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-right: 8px; vertical-align: -5px;"><path d="M13 8L17 12M17 12L13 16M17 12H3M8 8V7C8 5.34315 9.34315 4 11 4H18C19.6569 4 21 5.34315 21 7V17C21 18.6569 19.6569 20 18 20H11C9.34315 20 8 18.6569 8 17V16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
        
        modalAction.innerHTML = actionIcon + action;
        
        // Update confirm button
        confirmBtn.textContent = 'Confirm ' + action;
        confirmBtn.className = instructor.status === 'out' 
            ? 'confirm-btn time-in-btn' 
            : 'confirm-btn time-out-btn';
        
        // Add icon to confirm button
        const confirmIcon = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M5 13L9 17L19 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
        confirmBtn.innerHTML = confirmIcon + ' Confirm ' + action;

        // Show modal
        modal.style.display = 'flex';
        
        // Auto-confirm after 5 seconds
        let autoConfirmTimeout = setTimeout(() => {
            confirmAction();
        }, 5000);

        // Close modal function
        function closeModal() {
            modal.style.display = 'none';
            clearTimeout(autoConfirmTimeout);
            rfidInput.focus(); // Refocus the RFID input
        }

        // Confirm action function
        function confirmAction() {
            const { date, time } = getCurrentDateTime();
            
            if (instructor.status === 'out') {
                // Time in
                instructor.status = 'in';
                addLogEntry(instructor, date, time);
                showNotification(`${instructor.name} has successfully timed in at ${time}`, 'success');
            } else {
                // Time out
                instructor.status = 'out';
                updateLogEntry(instructor, time);
                showNotification(`${instructor.name} has successfully timed out at ${time}`, 'success');
            }
            
            closeModal();
        }

        // Event listeners
        document.getElementById('close-modal').addEventListener('click', closeModal);
        document.getElementById('close-modal-btn').addEventListener('click', closeModal);
        confirmBtn.addEventListener('click', confirmAction);
    }

    // Add log entry (time in)
    function addLogEntry(instructor, date, timeIn) {
        const logContainer = document.querySelector('.log-cards-container');
        
        // Create a new log card
        const logCard = document.createElement('div');
        logCard.className = 'log-card';
        logCard.setAttribute('data-rfid-id', instructor.id);
        
        // Card content
        logCard.innerHTML = `
            <div class="log-card-header">
                <div class="log-card-date">${date}</div>
                <div class="log-card-status time-in">Active</div>
            </div>
            <div class="log-card-body">
                <div class="log-card-photo">
                    <img src="${instructor.photoUrl || '../assets/profile-placeholder.jpg'}" alt="${instructor.name}">
                </div>
                <div class="log-card-details">
                    <h3>${instructor.name}</h3>
                    <p>${instructor.department}</p>
                    <p>${instructor.subject}</p>
                    <p>${instructor.section}</p>
                </div>
            </div>
            <div class="log-card-footer">
                <div class="log-time">
                    <div class="time-in-label">Time In</div>
                    <div class="time-in-value">${timeIn}</div>
                </div>
                <div class="time-out">
                    <div class="time-out-label">Time Out</div>
                    <div class="time-out-value">--:--</div>
                </div>
            </div>
        `;
        
        // Add the card to the container (at the beginning)
        if (logContainer.firstChild) {
            logContainer.insertBefore(logCard, logContainer.firstChild);
        } else {
            logContainer.appendChild(logCard);
        }
    }

    // Update log entry (time out)
    function updateLogEntry(instructor, timeOut) {
        const logCard = document.querySelector(`.log-card[data-rfid-id="${instructor.id}"]`);
        
        if (logCard) {
            // Update status
            const statusElement = logCard.querySelector('.log-card-status');
            statusElement.textContent = 'Completed';
            statusElement.className = 'log-card-status time-out';
            
            // Update time out
            const timeOutValue = logCard.querySelector('.time-out-value');
            timeOutValue.textContent = timeOut;
        }
    }

    // Show notification
    function showNotification(message, type = 'info') {
        const notification = document.getElementById('notification');
        
        // Set notification content and style
        notification.textContent = message;
        notification.className = type === 'error' ? 'error' : '';
        
        // Add show class to make notification visible
        notification.classList.add('show');
        
        // Hide notification after 3 seconds
        setTimeout(() => {
            notification.classList.remove('show');
        }, 3000);
    }

    // Handle RFID input
    rfidInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            const rfidId = this.value.trim();
            if (rfidId) {
                processRfidScan(rfidId);
                this.value = ''; // Clear the input
            }
        }
    });

    // Keep RFID input focused
    document.addEventListener('click', function() {
        rfidInput.focus();
    });
});
