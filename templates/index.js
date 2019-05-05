
var ws = new WebSocket("ws://localhost:8765/echo")
//建立web socket 连接成功触发事件
ws.onopen = function () {
 ws.send("客户端发送的数据")
 console.log("数据发送中....")
};
//接收 web socket 服务端数据时触发事件
ws.onmessage = function (evt) {
 var received_msg = evt.data
 console.log(received_msg)
};
//断开web socket 连接成功触发事件
ws.onclose = function () {
 console.log("连接已断开")
};
