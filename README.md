# EasyParentalControl
Parental control utility. Intended to limit browser use for 2h a day.

Client:
* Periodically retrieve the client configuration from server.
* Reports user activity to server.
* Show small topmost, half-transparent, un-closable window with countdown (guizero/tkinter).
* Kills internet browser when time has expired.

Server:
* Show howm much time has the user left today.
* Maintain the client configuration.
* Allow to configure each client via Web interface.

Version: 0.1

TODO:
+ client setup
+ server
+ server setup
