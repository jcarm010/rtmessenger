var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

var channel_connections = {};

app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});

io.on('connection', function(socket){
  console.log('a user connected');
  socket.on('disconnect', function(){
    console.log('user disconnected');
  });
  socket.on('request', function(request){
    console.log('message: ');
    console.log(request);
    try{
      //io.emit('chat message', msg);
      if(request.action === "subscribe"){
        console.log("Requested subscription");
        handleSubscribeRequest(request, socket);
      }else{
        throw "Invalid action type";
      }
      console.log("current channel connections:");
      for(var cname in channel_connections) {
        console.log(cname+": "+channel_connections[cname].length);
      }
    }catch (error){
      console.error(error);
      socket.disconnect()
    }
  });
  function handleSubscribeRequest(request, socket){
    var channelName = request.channel;
    if(channelName === null || channelName === undefined){
      throw "Invalid channel name: "+channelName;
    }
    var sockets = channel_connections[channelName];
    if(sockets === undefined){
      sockets = channel_connections[channelName] = [];
    }
    sockets.push(socket);
  }
});

http.listen(3000, function(){
  console.log('listening on *:3000');
});