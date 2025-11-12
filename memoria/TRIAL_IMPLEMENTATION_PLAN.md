# 🚀 Plano de Implementação - Trial Automático

**Data**: 12/11/2025  
**Versão**: v4.9  
**Prioridade**: CRÍTICA

---

## 📋 Especificações Aprovadas

```yaml
trial_config:
  duracao: 15 dias
  storage: 10 GB
  videos: Ilimitados
  upload_max: 1 GB por arquivo
  conversao: 1080p
  bandwidth: 20 GB/mes
  marca_dagua: false  # Removida para melhor experiência
  custo_estimado: $5.00 por trial
  
  lifecycle:
    pos_trial_7d: Mover para Glacier Instant Retrieval
    inativo_30d: Mover para Intelligent-Tiering
    inativo_90d: Mover para Glacier Instant Retrieval
    recuperacao: Automática ao login
```

---

## 🔧 Implementação Técnica

### FASE 1: Lambda create-user (Cadastro)

**Arquivo**: `aws-setup/lambda-functions/create-user/lambda_function.py`

```python
def lambda_handler(event, context):
    # Criar usuário com status 'trial' automático
    user_data = {
        'user_id': user_id,
        'email': email,
        'password_hash': hash_password(password),
        'status': 'trial',  # ← MUDANÇA: era 'pending'
        'role': 'user',
        'trial_start': datetime.now().isoformat(),
        'trial_end': (datetime.now() + timedelta(days=15)).isoformat(),
        'plan': 'trial',
        'limits': {
            'storage_gb': 10,
            'bandwidth_gb': 20,
            'upload_max_gb': 1,
            'conversao_max': '1080p'
        },
        'usage': {
            'storage_used_gb': 0,
            'bandwidth_used_gb': 0,
            'videos_count': 0
        }
    }
```

**Deploy**:
```bash
cd aws-setup/lambda-functions
python -c "import zipfile,os;z=zipfile.ZipFile('create-user-deploy.zip','w');[z.write(os.path.join(r,f),os.path.join(r,f).replace('create-user\\','')) for r,_,fs in os.walk('create-user') for f in fs];z.close()"
aws lambda update-function-code --function-name mediaflow-create-user --zip-file fileb://create-user-deploy.zip
```

---

### FASE 2: Lambda check-limits (Validação)

**Criar novo Lambda**: `check-limits`

```python
import boto3
import json
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    user_id = event['user_id']
    action = event['action']  # 'upload', 'bandwidth', 'trial'
    
    # Buscar usuário
    table = dynamodb.Table('mediaflow-users')
    user = table.get_item(Key={'user_id': user_id})['Item']
    
    # Verificar trial expirado
    if user['plan'] == 'trial':
        trial_end = datetime.fromisoformat(user['trial_end'])
        if datetime.now() > trial_end:
            return {
                'allowed': False,
                'reason': 'trial_expired',
                'message': 'Seu trial expirou. Faça upgrade para continuar.'
            }
    
    # Verificar storage
    if action == 'upload':
        file_size_gb = event['file_size'] / (1024**3)
        storage_used = user['usage']['storage_used_gb']
        storage_limit = user['limits']['storage_gb']
        
        if storage_used + file_size_gb > storage_limit:
            return {
                'allowed': False,
                'reason': 'storage_limit',
                'message': f'Limite de {storage_limit} GB atingido. Faça upgrade.'
            }
        
        # Verificar tamanho do arquivo
        upload_max = user['limits']['upload_max_gb']
        if file_size_gb > upload_max:
            return {
                'allowed': False,
                'reason': 'file_too_large',
                'message': f'Arquivo maior que {upload_max} GB. Limite do plano.'
            }
    
    # Verificar bandwidth
    if action == 'bandwidth':
        bandwidth_used = user['usage']['bandwidth_used_gb']
        bandwidth_limit = user['limits']['bandwidth_gb']
        
        if bandwidth_used > bandwidth_limit:
            return {
                'allowed': False,
                'reason': 'bandwidth_limit',
                'message': f'Limite de {bandwidth_limit} GB/mês atingido.'
            }
    
    return {'allowed': True}
```

**Criar Lambda**:
```bash
aws lambda create-function \
  --function-name mediaflow-check-limits \
  --runtime python3.11 \
  --role arn:aws:iam::969430605054:role/mediaflow-lambda-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://check-limits.zip \
  --timeout 10
```

---

### FASE 3: S3 Lifecycle Policy

**Arquivo**: `configure-lifecycle.py`

```python
import boto3

s3 = boto3.client('s3')
bucket = 'mediaflow-uploads-969430605054'

lifecycle_config = {
    'Rules': [
        {
            'Id': 'trial-to-glacier-7d',
            'Status': 'Enabled',
            'Filter': {'Prefix': 'users/'},
            'Transitions': [
                {
                    'Days': 7,
                    'StorageClass': 'GLACIER_IR'
                }
            ],
            'Expiration': {'Days': 120}
        },
        {
            'Id': 'inactive-to-intelligent-30d',
            'Status': 'Enabled',
            'Filter': {'Prefix': 'users/'},
            'Transitions': [
                {
                    'Days': 30,
                    'StorageClass': 'INTELLIGENT_TIERING'
                }
            ]
        },
        {
            'Id': 'inactive-to-glacier-90d',
            'Status': 'Enabled',
            'Filter': {'Prefix': 'users/'},
            'Transitions': [
                {
                    'Days': 90,
                    'StorageClass': 'GLACIER_IR'
                }
            ]
        }
    ]
}

s3.put_bucket_lifecycle_configuration(
    Bucket=bucket,
    LifecycleConfiguration=lifecycle_config
)

print("Lifecycle configurado!")
```

---

### FASE 4: Lambda send-trial-emails

**Criar Lambda com EventBridge**:

```python
import boto3
from datetime import datetime, timedelta

ses = boto3.client('ses')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table('mediaflow-users')
    
    # Buscar trials expirados
    response = table.scan(
        FilterExpression='plan = :trial',
        ExpressionAttributeValues={':trial': 'trial'}
    )
    
    for user in response['Items']:
        trial_end = datetime.fromisoformat(user['trial_end'])
        days_since_trial = (datetime.now() - trial_end).days
        
        # Email D+0
        if days_since_trial == 0:
            send_email(user['email'], 'trial_expired', user)
        
        # Email D+7 (50% OFF)
        elif days_since_trial == 7:
            send_email(user['email'], 'last_chance', user)
        
        # Email D+30 (3 meses)
        elif days_since_trial == 30:
            send_email(user['email'], 'comeback', user)
        
        # Email D+90 (aviso exclusão)
        elif days_since_trial == 90:
            send_email(user['email'], 'deletion_warning', user)

def send_email(to, template, user):
    templates = {
        'trial_expired': {
            'subject': 'Seu trial expirou - Continue de onde parou',
            'body': f'''
                Olá {user['name']},
                
                Seu trial de 15 dias expirou. Seus vídeos estão seguros e acessíveis.
                
                Faça upgrade para continuar:
                - Basic: $19.99/mês (50 GB)
                - Pro: $39.99/mês (200 GB)
                
                [Fazer Upgrade]
            '''
        },
        'last_chance': {
            'subject': '50% OFF - Última chance antes do arquivamento',
            'body': f'''
                Olá {user['name']},
                
                Última chance! Use o cupom VOLTA50 para 50% OFF no primeiro mês.
                
                Seus vídeos serão arquivados amanhã (mas não deletados).
                
                [Ativar com Desconto]
            '''
        }
        # ... outros templates
    }
    
    ses.send_email(
        Source='noreply@midiaflow.com',
        Destination={'ToAddresses': [to]},
        Message={
            'Subject': {'Data': templates[template]['subject']},
            'Body': {'Text': {'Data': templates[template]['body']}}
        }
    )
```

**EventBridge Rule** (executar diariamente):
```bash
aws events put-rule \
  --name mediaflow-trial-emails \
  --schedule-expression "cron(0 10 * * ? *)"
  
aws events put-targets \
  --rule mediaflow-trial-emails \
  --targets "Id"="1","Arn"="arn:aws:lambda:us-east-1:969430605054:function:mediaflow-send-trial-emails"
```

---

### FASE 5: Frontend - Dashboard

**Arquivo**: `app/dashboard/page.tsx`

```typescript
// Adicionar ao useEffect
useEffect(() => {
  const checkTrialStatus = async () => {
    const user = JSON.parse(localStorage.getItem('current_user'))
    
    if (user.plan === 'trial') {
      const trialEnd = new Date(user.trial_end)
      const daysLeft = Math.ceil((trialEnd - new Date()) / (1000 * 60 * 60 * 24))
      
      if (daysLeft <= 0) {
        // Trial expirado
        setShowUpgradeModal(true)
      } else {
        // Mostrar badge
        setTrialDaysLeft(daysLeft)
      }
    }
  }
  
  checkTrialStatus()
}, [])

// Adicionar badge no header
{currentUser?.plan === 'trial' && (
  <div className="badge-trial">
    Trial: {trialDaysLeft} dias restantes
    <button onClick={() => router.push('/pricing')}>
      Fazer Upgrade
    </button>
  </div>
)}

// Adicionar progresso
{currentUser?.plan === 'trial' && (
  <div className="trial-progress">
    <div>Storage: {currentUser.usage.storage_used_gb} / 10 GB</div>
    <div>Bandwidth: {currentUser.usage.bandwidth_used_gb} / 20 GB</div>
  </div>
)}
```

---

## 📊 Custos Estimados

```
Por Trial (15 dias):
├─ Storage: 10 GB × $0.023 = $0.23
├─ Bandwidth: 20 GB × $0.09 = $1.80
├─ CloudFront: 20 GB × $0.085 = $1.70
├─ Conversão 1080p: ~$0.50
└─ TOTAL: ~$5.00

Com Lifecycle (após 7 dias):
├─ Storage Glacier: 10 GB × $0.004 = $0.04/mês
├─ Economia: 83%
└─ Custo anual por trial não convertido: $0.48
```

---

## ✅ Checklist de Deploy

- [ ] Atualizar Lambda create-user
- [ ] Criar Lambda check-limits
- [ ] Configurar S3 Lifecycle
- [ ] Criar Lambda send-trial-emails
- [ ] Configurar EventBridge
- [ ] Atualizar Dashboard frontend
- [ ] Criar página /pricing
- [ ] Testar fluxo completo
- [ ] Deploy em produção

---

**Próximo passo**: Implementar Lambda create-user?
