@echo off
aws s3 sync "C:\Users\dell 5557\Videos\IDM\Star" s3://mediaflow-uploads-969430605054/sergio/Star/ --exclude "*" --include "*.mp4" --no-progress
