var ws = new WebSocket("ws://192.168.0.104/ws");

function chooseAlgorithm(){
    var form = document.getElementsByClassName("algorithm-form")

    var val

    //var radios = form.getElementsByName("algo")
    var radios = document.getElementsByName("algo")

    var len = radios.length

    for(var i = 0; i < len; i++)
    {
        if(radios[i].checked)
        {
            val = radios[i].value
            break;
        }
    }

    var message = "a" + val

    ws.send(message)
}