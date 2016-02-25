var wsUrl = $("meta[name='wsUrl']").attr("content");

var sock = new SockJS(wsUrl);

sock.onmessage = function(e) {
    console.log(e)
    if(e.data.is_browser_notification && window.Notification && Notification.permission !== "denied") {
        Notification.requestPermission(function(status) {  // status is "granted", if accepted by user
            var n = new Notification(e.data.title, {
                body: e.data.message,
            });
        });
    }
 };
