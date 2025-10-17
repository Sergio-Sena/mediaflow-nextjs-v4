@echo off
echo ========================================
echo  Deploy Lambdas - Mediaflow v4.4
echo ========================================
echo.

echo [1/4] Atualizando auth-handler...
cd lambda-functions\auth-handler
del auth.zip 2>nul
powershell -Command "Compress-Archive -Path lambda_function.py -DestinationPath auth.zip -Force"
aws lambda update-function-code --function-name mediaflow-auth-handler --zip-file fileb://auth.zip --region us-east-1
cd ..\..
echo.

echo [2/4] Atualizando files-handler...
cd lambda-functions\files-handler
del files-handler.zip 2>nul
powershell -Command "Compress-Archive -Path lambda_function.py -DestinationPath files-handler.zip -Force"
aws lambda update-function-code --function-name mediaflow-list-files --zip-file fileb://files-handler.zip --region us-east-1
cd ..\..
echo.

echo [3/4] Atualizando usuarios no DynamoDB...
python update-users-s3-prefix.py
echo.

echo [4/4] Aguardando propagacao (10s)...
timeout /t 10 /nobreak
echo.

echo ========================================
echo  Deploy concluido!
echo ========================================
echo.
echo Proximos passos:
echo 1. Teste o login com cada usuario
echo 2. Verifique se cada um ve apenas seus arquivos
echo 3. Admin deve ver tudo
echo.
pause
