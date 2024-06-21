document.addEventListener("DOMContentLoaded", function() {
    function updateTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString();
        document.getElementById("current-time").textContent = timeString;
    }

    function updateCalendar() {
        const now = new Date();
        const month = now.getMonth();
        const year = now.getFullYear();
        const firstDayOfMonth = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        const currentDate = now.getDate();

        const monthNames = ["January", "February", "March", "April", "May", "June", 
                            "July", "August", "September", "October", "November", "December"];
        
        document.getElementById("current-month").textContent = `${monthNames[month]} ${year}`;
        
        const calendarDates = document.getElementById("calendar-dates");
        calendarDates.innerHTML = "";

        // Add empty divs for days of the previous month
        for (let i = 0; i < firstDayOfMonth; i++) {
            const emptyDiv = document.createElement("div");
            emptyDiv.classList.add("empty");
            calendarDates.appendChild(emptyDiv);
        }

        // Add divs for each day of the current month
        for (let day = 1; day <= daysInMonth; day++) {
            const dateDiv = document.createElement("div");
            dateDiv.textContent = day;
            if (day === currentDate) {
                dateDiv.classList.add("current-day");
            }
            calendarDates.appendChild(dateDiv);
        }
    }

    updateTime();
    updateCalendar();
    setInterval(updateTime, 1000); // Update time every second
});
