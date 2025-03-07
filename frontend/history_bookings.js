document.addEventListener('DOMContentLoaded', () => {
    updateDateTime();
    setInterval(updateDateTime, 60000); // Update every minute
    loadBookings();
});

function updateDateTime() {
    const now = new Date();
    const dateOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const timeOptions = { hour: '2-digit', minute: '2-digit', hour12: true };
    
    document.getElementById('current-date').textContent = now.toLocaleDateString('en-US', dateOptions);
    document.getElementById('current-time').textContent = now.toLocaleTimeString('en-US', timeOptions);
}

function loadBookings() {
    // Sample data - replace with actual API call in production
    const bookings = [
        {
            date: '11/6/2024',
            timeSlot: '9:00 am - 12:00 am',
            purpose: 'Web Applications Development 2',
            section: 'BSIT-2A',
            labRoom: 'L202',
            status: 'pending'
        },
        {
            date: '10/30/2024',
            timeSlot: '9:00 am - 12:00 am',
            purpose: 'Web Applications Development 2',
            section: 'BSIT-2A',
            labRoom: 'L202',
            status: 'approved'
        },
        {
            date: '10/23/2024',
            timeSlot: '9:00 am - 12:00 am',
            purpose: 'Web Applications Development 2',
            section: 'BSIT-2A',
            labRoom: 'L202',
            status: 'rejected'
        },
        {
            date: '10/16/2024',
            timeSlot: '9:00 am - 12:00 am',
            purpose: 'Web Applications Development 2',
            section: 'BSIT-2A',
            labRoom: 'L202',
            status: 'cancelled'
        }
    ];

    const bookingsList = document.getElementById('bookings-list');
    bookingsList.innerHTML = '';

    bookings.forEach(booking => {
        const bookingRow = document.createElement('div');
        bookingRow.className = 'booking-row';
        bookingRow.innerHTML = `
            <div>${booking.date}</div>
            <div>${booking.timeSlot}</div>
            <div>${booking.purpose}</div>
            <div>${booking.section}</div>
            <div>${booking.labRoom}</div>
            <div>
                <span class="status ${booking.status.toLowerCase()}">${capitalizeFirstLetter(booking.status)}</span>
            </div>
        `;
        bookingsList.appendChild(bookingRow);
    });
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

// Filter dropdown functionality
document.querySelector('.filter-btn').addEventListener('click', () => {
    // Implement filter dropdown
    console.log('Filter clicked');
});

// Sort dropdown functionality
document.querySelector('.sort-btn').addEventListener('click', () => {
    // Implement sort dropdown
    console.log('Sort clicked');
});

// Book schedule button functionality
document.querySelector('.book-schedule-btn').addEventListener('click', () => {
    // Implement booking schedule
    console.log('Book schedule clicked');
});
