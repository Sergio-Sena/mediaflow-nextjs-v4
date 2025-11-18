import boto3
import os
from pathlib import Path

rekognition = boto3.client('rekognition', region_name='us-east-1')
folder_path = r"C:\Users\dell 5557\Pictures\imagens devagram"

images = list(Path(folder_path).glob('*.[jJ][pP][gG]')) + \
         list(Path(folder_path).glob('*.[pP][nN][gG]')) + \
         list(Path(folder_path).glob('*.[gG][iI][fF]'))

print(f"#SouVoluntario - Descrevendo {len(images)} imagens:\n")

for img_path in sorted(images):
    with open(img_path, 'rb') as img_file:
        response = rekognition.detect_labels(
            Image={'Bytes': img_file.read()},
            MaxLabels=5,
            MinConfidence=70
        )
    
    labels = [label['Name'] for label in response['Labels']]
    print(f"📸 {img_path.name}")
    print(f"   {', '.join(labels)}\n")
