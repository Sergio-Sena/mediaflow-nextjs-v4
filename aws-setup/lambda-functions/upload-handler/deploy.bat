@echo off
echo Criando pacote da Lambda upload-handler...

cd /d "%~dp0"

if exist function.zip del function.zip

powershell -Command "Compress-Archive -Path lambda_function.py,jwt -DestinationPath function.zip -Force"

echo.
echo Fazendo deploy para AWS Lambda...
aws lambda update-function-code --function-name mediaflow-upload-handler --zip-file fileb://function.zip --region us-east-1

echo.
echo Deploy concluido!
pause
