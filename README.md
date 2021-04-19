# DirezioneInvestigativaAntimafia-DIA-
Repository per il progetto di Data and Intelligence Applications

Progetto di DIA  

| Functionality | State |
|:-----------------------|:------------------------------------:|
| Try | [todo](#) |
| Complete rules | [![GREEN](https://placehold.it/15/44bb44/44bb44)](#)|
| Socket | [![YELLOW](https://placehold.it/15/44bb44/44bb44)](#) |
| RMI | [![RED](https://placehold.it/15/f03c15/f03c15)](#) |
| GUI | [![YELLOW](https://placehold.it/15/44bb44/44bb44)](#) |
| CLI | [![GREEN](https://placehold.it/15/44bb44/44bb44)](#) |
| Multiple games | [![GREEN](https://placehold.it/15/44bb44/44bb44)](#) |
| Persistence |[![RED](https://placehold.it/15/f03c15/f03c15)](#) |
| Domination or Towers modes | [![RED](https://placehold.it/15/f03c15/f03c15)](#) |
| Terminator | [![RED](https://placehold.it/15/f03c15/f03c15)](#) |



To launch our project, the client.jar and server.jar files must be into a specific folder. There must be three sub-folders: 
one named "database", another one with the javafx package (11.0.2 version) and a third one called LoggerFiles that contains 
other two folders, Client and Server. The javafx package is present on the repository as a .zip file, so before
going on you'll need to unzip it.
To star the server.jar, you'll have to write on the command line "java -jar server.jar" and it will be ready, while for the client.jar
you'll have to write "java -jar --module-path ./javafx-sdk-11.0.2/lib --add-modules=javafx.controls client.jar", which will 
start the client adding the right javafx modules so that the GUI will be started properly.
When the client is on, the first thing you'll see is that the command line is asking you if you prefer using the CLI or the
GUI, and after that you'll have to write the username you want and the IP address of the machine that started the server.
After the log in is confirmed as legal, if you are the first player that logged in, you'll decide on which board the game will take place and how many deaths there
will be before the final frenzy. If you're not the first, you'll just have to wait for a few seconds. 
After that, your Adrenaline game is going to begin!
