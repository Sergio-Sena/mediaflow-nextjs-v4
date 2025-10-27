@echo off
echo Uploading Star folder to S3...
echo Source: C:\Users\dell 5557\Videos\IDM\Star
echo Destination: s3://mediaflow-uploads-969430605054/users/user_admin/Star/
echo.

aws s3 sync "C:\Users\dell 5557\Videos\IDM\Star" s3://mediaflow-uploads-969430605054/users/user_admin/Star/ --storage-class INTELLIGENT_TIERING --no-progress

echo.
echo Upload completed!
pause