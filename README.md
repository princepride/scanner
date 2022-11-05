# Scanner
you can use your mobile phone or PC to take a photo, then the photo will send to the backend and it will return a string to the frontend
## Add Models
go to the [google driver](https://drive.google.com/drive/folders/1J2g8viWP9A3dokd7MuZAFtRqJ1JCA67y?usp=sharing) to install the models and move it to the file path `scanner/backend/`
## Backend
`$ cd backend`  
`$ pip install -r requirement.txt`  
`$ python app.py` (change the host based on your address)

## Frontend
`$ cd frontend`  
`$ npm install`  
**Windows (Powershell)**  
`$ ($env:HTTPS = "true") -and (npm start)`  
**Windows (cmd.exe)**  
`$ set HTTPS=true&&npm start`  
**Linux, macOS (Bash)**  
`$ HTTPS=true npm start`
