# EasyParentalControl
Parental control utility. Intended to limit browser use for 2h a day.

Client:
* Periodically retrieve the client configuration from server.
* Reports user activity to server.
* Show small topmost, half-transparent, un-closable window with countdown (uses 3rd party source-code Guizero which adds tkinter dependency).
* Kills internet browser when time has expired.
* Install on Raspberry pi by: $sudo ./install_client.sh

Server:
* Show howm much time has the user left today.
* Maintain the client configuration.
* Allow to configure each client via Web interface (uses 3rd party source code: Bottle).
* uses bottle for https server

Version: 0.1

TODO:
+ client setup
+ server
+ server setup
