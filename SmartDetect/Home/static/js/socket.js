var connection = new signalR.HubConnectionBuilder().withUrl("http://120.72.98.68:8099/chathub").build();
connection.on("ReceiveMessage", function (user, message) {
    console.log(user + ": " + message);
});
connection.start().then(function () {
    console.log("Socket ready!")
}).catch(function (err) {
    return console.error(err.toString());
});
function sendMessage(){
    var user = "Arino"
    var message = "HelloWorld"
    connection.invoke("SendMessage", user, message).catch(function (err) {
        return console.error(err.toString());
    });
}