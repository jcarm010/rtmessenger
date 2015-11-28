var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});

var channel_connections = {};
var socket_connections = {};

io.on('connection', function(socket){
  console.log('a user connected');
  socket_connections[socket] = [];
  socket.on('disconnect', function(){
    console.log('user disconnected');
    var channels = socket_connections[socket];
    for(var i = 0 ; i < channels.length; i++){
      var channel = channels[i];
      io.emit(channel, {channel: channel, presence:true, message: {name:'test', action:"left"}});
    }
    delete socket_connections[socket];
  });
  socket.on('request', function(request){
    console.log('message: ');
    console.log(request);
    try{
      //io.emit('chat message', msg);
      if(request.action === "subscribe"){
        console.log("Requested subscription");
        handleSubscribeRequest(request, socket);
      }else if(request.action === "message"){
        handleMessage(request, socket);
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
  function handleMessage(request, socket){
    var channelName = request.channel;
    io.emit(channelName, {channel: channelName,presence:false, message: request.message});
  }
  function handleSubscribeRequest(request, socket){
    var channelName = request.channel;
    if(channelName === null || channelName === undefined){
      socket.emit("subscribed", {success:false, channel: channelName, message:"Invalid channel name: "+channelName});
      throw "Invalid channel name: "+channelName;
    }
    var sockets = channel_connections[channelName];
    if(sockets === undefined){
      sockets = channel_connections[channelName] = [];
    }
    sockets.push(socket);
    socket_connections[socket].push(channelName);
    socket.emit("subscribed", {success:true, channel:channelName});
    io.emit(channelName, {channel: channelName, presence:true, message: {name:'test', action:"joined"}});
  }
});

module.exports = {
  app: app,
  io:io
};