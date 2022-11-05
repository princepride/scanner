# scanner
you can use your mobile phone or PC to take a photo, then the photo will send to the backend and it will return a string to the frontend
## backend
`$ cd backend`  
`$ python app.py` (change the host based on your address)

## frontend
`$ cd frontend`  
**Windows (Powershell)**  
`$ ($env:HTTPS = "true") -and (npm start)`  
**Windows (cmd.exe)**  
`$ set HTTPS=true&&npm start`  
**Linux, macOS (Bash)**  
`$ HTTPS=true npm start`
