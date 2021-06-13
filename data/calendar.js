//const calendar = document.querySelector("#app-calendar")

var ws = new WebSocket("ws://192.168.0.104/ws");

ws.onopen = function() {
    ws.send("u"); // when page is loaded check if the client is logged
}

ws.onmessage = function(evt){
    if(evt.data[0] == 'i')
    {
        console.log(evt.data);
        var pers = evt.data.substring(1);
        splited = pers.split(",");
        if(pers[0] == 'T')
            document.querySelector(".stats").innerHTML = pers;
        else
            document.querySelector(".stats").innerHTML = "Total persons which walked over the gate: " + splited[0] + 
                                                            ". People which walked inside: " + splited[1] + 
                                                            ". People which walked outside: " + splited[2] + ".";
    }
    else if(evt.data[0] == 'p')
    {
        res = evt.data.substring(1);

        if(res[0] == '0')
            window.location.href = "/login";
    }
}

var currentDisplayedMonth;
var calendar = document.querySelector("#app-calendar");
var prev;

const isWeekend = day => {
    return day === 6 || day === 0;
}

/*const timeElapsed = Date.now();
const today = new Date(timeElapsed);
let month = "";
let prevMonth = "";
let nextMonth = "";
switch(today.getMonth()){
    case 0 : month = "Ianuarie";
             prevMonth = "Decembrie"
             nextMonth = "Februarie";
             break;
    case 1 : month = "Februarie";
             prevMonth = "Ianuarie";
             nextMonth = "Martie";
             break;
    case 2 : month = "Martie";
             prevMonth = "Februarie";
             nextMonth = "Aprilie";
             break;
    case 3 : month = "Aprilie";
             prevMonth = "Martie";
             nextMonth = "Mai";
             break;
    case 4 : month = "Mai";
             prevMonth = "Aprilie";
             nextMonth = "Iunie";
             break;
    case 5 : month = "Iunie";
             prevMonth = "Mai";
             nextMonth = "Iulie";
             break;
    case 6 : month = "Iulie";
             prevMonth = "Iunie";
             nextMonth = "August";
             break;
    case 7 : month = "August";
             prevMonth = "Iulie";
             nextMonth = "Septembrie";
             break;
    case 8 : month = "Septembrie";
             prevMonth = "August";
             nextMonth = "Octombrie";
             break;
    case 9 : month = "Octombrie";
             prevMonth = "Septembrie";
             nextMonth = "Noiembrie";
             break;
    case 10: month = "Noiembrie";
             prevMonth = "Octombrie";
             nextMonth = "Decembrie";
             break;
    case 11: month = "Decembrie";
             prevMonth = "Noiembrie";
             nextMonth = "Ianuarie";
             break;
}
calendar.insertAdjacentHTML("beforebegin", `<div class="month"><div class="prev-month">${prevMonth}</div>${month}<div class="next-month">${nextMonth}</div></div>`)*/

const getDayName = function(year, month, day) {
    const date = new Date(year, month, day);
    const options = { weekday: "long"};
    return new Intl.DateTimeFormat("ro-RO", options).format(date);
}

const getDaysInCurrentMonth = function(year, month){
    let date = new Date(year, month + 1, 0);
    return date.getDate();
}

const getFirstDayIndex = function(year, month){
    const date = new Date(year, month, 0);
    return date.getDay();
}

const getDayIndex = function(year, month, day){
    const date = new Date(year, month, day);
    return date.getDay();
}

/*let noOfDays = getDaysInCurrentMonth();
for(let day = 1; day <= noOfDays; day++){
    const weekend = isWeekend(day)
    const dayName = getDayName(day)
    calendar.insertAdjacentHTML("beforeend", `<div class="day ${weekend ? "weekend" : ""}"><div class="name">${dayName}</div>${day}</div>`);
}

document.querySelectorAll("#app-calendar .day").forEach
(day => {
    day.addEventListener("click", event => {
        event.currentTarget.classList.toggle("selected");
    });
});*/
const showCalendar = function(currentYear, currentMonth) {

    currentDisplayedMonth = new Date(currentYear, currentMonth, 1);
    let month = "";
    let prevMonth = "";
    let nextMonth = "";
    switch(currentDisplayedMonth.getMonth()){
        case 0 : month = "Ianuarie";
                prevMonth = "Decembrie"
                nextMonth = "Februarie";
                break;
        case 1 : month = "Februarie";
                prevMonth = "Ianuarie";
                nextMonth = "Martie";
                break;
        case 2 : month = "Martie";
                prevMonth = "Februarie";
                nextMonth = "Aprilie";
                break;
        case 3 : month = "Aprilie";
                prevMonth = "Martie";
                nextMonth = "Mai";
                break;
        case 4 : month = "Mai";
                prevMonth = "Aprilie";
                nextMonth = "Iunie";
                break;
        case 5 : month = "Iunie";
                prevMonth = "Mai";
                nextMonth = "Iulie";
                break;
        case 6 : month = "Iulie";
                prevMonth = "Iunie";
                nextMonth = "August";
                break;
        case 7 : month = "August";
                prevMonth = "Iulie";
                nextMonth = "Septembrie";
                break;
        case 8 : month = "Septembrie";
                prevMonth = "August";
                nextMonth = "Octombrie";
                break;
        case 9 : month = "Octombrie";
                prevMonth = "Septembrie";
                nextMonth = "Noiembrie";
                break;
        case 10: month = "Noiembrie";
                prevMonth = "Octombrie";
                nextMonth = "Decembrie";
                break;
        case 11: month = "Decembrie";
                prevMonth = "Noiembrie";
                nextMonth = "Ianuarie";
                break;
    }
    calendar.insertAdjacentHTML("beforebegin", `<div class="month"><div class="prev-month">< ${prevMonth}</div>${month} ${currentYear}<div class="next-month">${nextMonth} ></div></div>`)

    const dayNames = ["Luni", "Marti", "Miercuri", "Joi", "Vineri", "Sambata", "Duminica"];

    dayNames.forEach(dayName => {
        calendar.insertAdjacentHTML("beforeend", `<div class="day-name">${dayName}</div>`)
    })

    let firstDayIndex = getFirstDayIndex(currentYear, currentMonth);
    while(firstDayIndex > 0)
    {
        calendar.insertAdjacentHTML("beforeend", `<div class="prev-month-day"></div>`);
        firstDayIndex--;
    }

    let noOfDays = getDaysInCurrentMonth(currentDisplayedMonth.getFullYear(), currentDisplayedMonth.getMonth());
    for(let day = 1; day <= noOfDays; day++){
        let dayIndex = getDayIndex(currentYear, currentMonth, day);
        const weekend = isWeekend(dayIndex)
        const dayName = getDayName(currentYear, currentMonth, day)
        calendar.insertAdjacentHTML("beforeend", `<div class="day ${weekend ? "weekend" : ""} ${day === today.getDate() ? "selected" : ""}">${day}</div>`);
    }

    prev = document.querySelector(".prev-month");


    prev.addEventListener("click", event => {
        var m = document.querySelector(".month");
        document.querySelectorAll(".day-name").forEach
        (dayName => {
            dayName.remove();
        });
        document.querySelectorAll(".day").forEach
        (day => {
            day.remove();
        });
        m.remove();
        document.querySelectorAll(".prev-month-day").forEach
        (
            prevMonthDay => {
                prevMonthDay.remove();
            }
        );
        console.log(prev)
        if(currentDisplayedMonth.getMonth() == 0)
        {
            showCalendar(currentDisplayedMonth.getFullYear() - 1, 11);
        }
        else 
        {
            showCalendar(currentDisplayedMonth.getFullYear(), currentDisplayedMonth.getMonth() - 1);
        }
    })

    var next = document.querySelector(".next-month");
    next.addEventListener("click", event => {
    var m = document.querySelector(".month");
    document.querySelectorAll(".day-name").forEach
        (dayName => {
            dayName.remove();
        });
    document.querySelectorAll(".day").forEach
    (day => {
        day.remove();
    });

    document.querySelectorAll(".prev-month-day").forEach
    (
        prevMonthDay => {
            prevMonthDay.remove();
        }
    );
    m.remove();
    if(currentDisplayedMonth.getMonth() == 11)
    {
        showCalendar(currentDisplayedMonth.getFullYear() + 1, 0);
    }
    else
    {
        showCalendar(currentDisplayedMonth.getFullYear(), currentDisplayedMonth.getMonth() + 1);
    }
})

    document.querySelectorAll("#app-calendar .day").forEach
    (day => {
        day.addEventListener("click", event => {
            var month = currentDisplayedMonth.getMonth() + 1;
            if(month < 10)
                month = "0" + month;
            var message = "i" + currentDisplayedMonth.getFullYear() + "," + month + "," + day.innerHTML;
            console.log(message);
            ws.send(message);
        });
    });
}

const timeElapsed = Date.now();
let today = new Date(timeElapsed);
showCalendar(today.getFullYear(), today.getMonth());

//prev = document.querySelector(".prev-month");
/*prev.addEventListener("click", event => {
    var m = document.querySelector(".month");
    document.querySelectorAll(".day").forEach
    (day => {
        day.remove();
    });
    m.remove();
    console.log(prev)
    showCalendar(currentDisplayedMonth.getFullYear(), currentDisplayedMonth.getMonth() - 1);
})*/

/*var next = document.querySelector(".next-month");
next.addEventListener("click", event => {
    var m = document.querySelector(".month");
    document.querySelectorAll(".day").forEach
    (day => {
        day.remove();
    });
    m.remove();
    showCalendar(currentDisplayedMonth.getFullYear(), currentDisplayedMonth.getMonth() + 1);
})*/


