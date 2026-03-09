@echo off
echo Enviando arquivo de 7GB para S3...
echo.

aws s3 cp "C:\Users\dell 5557\Videos\IDM\Anime\RE4\4 Hours Of Resident Evil.mp4" s3://mediaflow-uploads-969430605054/users/user_admin/Anime/RE4/4_Hours_Of_Resident_Evil.mp4

echo.
echo Upload concluido!
pause
