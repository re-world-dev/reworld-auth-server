port : 9606

request : b"<type (hex)>-<arg1>-<arg2>-<arg3...>"

### Types (from the client)
\x00 : account creation (arg1:username, arg2: password)
\x01 : login
\x02 : connexion to a server
\x03 : disconnexion to a server
\x04 : logout

### Types (from the a.s.)
\x00 : task failed (arg1:error code, arg2:reason)
\x01 : task ok

### Error codes
0 : unknow
1 : username taken
2 : bad identification