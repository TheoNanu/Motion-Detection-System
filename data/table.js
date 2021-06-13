var ws = new WebSocket("ws://192.168.0.104/ws");
var isLogged = false;
const table = document.querySelector(".data-table");

ws.onopen = function() {
    ws.send("u");
    ws.send("r");
};

ws.onmessage = function(evt) {

    /*var resp = evt.data.split(";")
    var date = resp[2];
    var res = date.split(",")

    table.insertAdjacentHTML("beforeend", 
        `<tr>
            <td>${res[0]}</td>
            <td>${res[1]}</td>
            <td>${res[2]}</td>
            <td>${resp[0]}</td>
        </tr>`);*/

   /* document.querySelectorAll(".data-row").forEach(
        row => {
            if(row != null)
            {
                row.remove();
            }
        }
    );*/
    
    if(evt.data[0] == 'd'){
        var str = evt.data.substring(1);

        var res = str.split("\n");

        for(i = 0; i < res.length-1; i++){
            date = res[i].split(",");
            table.insertAdjacentHTML("beforeend", 
        `<tr class="data-row">
            <td>${date[0]}</td>
            <td>${date[1]}</td>
            <td>${date[2]}</td>
            <td>${date[3]}</td>
            <td>${date[4]}</td>
            <td>${date[5]}</td>
        </tr>`);

        }
        console.log(evt.data);
        //console.log(date[0]);
        //console.log(date[1]);
        //console.log(date[2]);
        //console.log(date[0]);
    }
    else if(evt.data[0] == 'p')
    {
        res = evt.data.substring(1);

        if(res[0] == '0')
            window.location.href = "/login";
        else
            isLogged = true;
    }
};