import boto3
import hashlib
import pyotp
import qrcode
import io
import base64

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1')
table = dynamodb.Table('mediaflow-users')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

users_config = [
    {
        'user_id': 'Lid',
        'name': 'Lid',
        'email': 'lid@sstech',
        'password': 'lid123'
    },
    {
        'user_id': 'Sergio_sena',
        'name': 'Sergio sena',
        'email': 'sena@sstech',
        'password': 'sena123'
    }
]

print("=== CONFIGURANDO CREDENCIAIS DE USUARIOS ===\n")

for user_config in users_config:
    user_id = user_config['user_id']
    
    # Gerar TOTP secret unico
    totp_secret = pyotp.random_base32()
    totp_uri = pyotp.totp.TOTP(totp_secret).provisioning_uri(
        name=user_config['email'],
        issuer_name='Mediaflow'
    )
    
    # Gerar QR Code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(totp_uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Salvar QR Code no S3
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    qr_key = f'qrcodes/qr_{user_id}.png'
    s3.put_object(
        Bucket='mediaflow-uploads-969430605054',
        Key=qr_key,
        Body=buffer,
        ContentType='image/png'
    )
    
    qr_url = f"https://mediaflow-uploads-969430605054.s3.amazonaws.com/{qr_key}"
    
    # Atualizar DynamoDB
    table.update_item(
        Key={'user_id': user_id},
        UpdateExpression='SET email = :email, password = :password, totp_secret = :totp, qr_code_url = :qr',
        ExpressionAttributeValues={
            ':email': user_config['email'],
            ':password': hash_password(user_config['password']),
            ':totp': totp_secret,
            ':qr': qr_url
        }
    )
    
    print(f"{user_config['name']}:")
    print(f"  Email: {user_config['email']}")
    print(f"  Senha: {user_config['password']}")
    print(f"  2FA Secret: {totp_secret}")
    print(f"  QR Code: {qr_url}")
    print()

print("=== CREDENCIAIS CONFIGURADAS ===")
print("\nPara testar 2FA, use Google Authenticator e escaneie os QR codes:")
print("- Lid: https://mediaflow-uploads-969430605054.s3.amazonaws.com/qrcodes/qr_Lid.png")
print("- Sergio_sena: https://mediaflow-uploads-969430605054.s3.amazonaws.com/qrcodes/qr_Sergio_sena.png")
