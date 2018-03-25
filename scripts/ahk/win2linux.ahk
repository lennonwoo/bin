#Include Socket.ahk

#w::
	x := new SocketTCP()
	x.Connect(["10.0.2.2", 1090])
	x.SendText("win2linux")
	x.Disconnect()
return