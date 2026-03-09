import boto3

s3 = boto3.client('s3')
BUCKET = 'mediaflow-uploads-969430605054'
USER_PREFIX = 'users/sergio_sena/'

def check_sergio_structure():
    """Mapeia a estrutura atual do sergio_sena"""
    print("📁 Estrutura atual do sergio_sena:\n")
    
    try:
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=BUCKET, Prefix=USER_PREFIX)
        
        root_files = []
        subfolders = {}
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    key = obj['Key']
                    relative_path = key.replace(USER_PREFIX, '')
                    
                    if not relative_path:  # Pasta vazia
                        continue
                    
                    size_mb = round(obj['Size'] / (1024*1024), 2)
                    
                    # Arquivo na raiz
                    if '/' not in relative_path:
                        root_files.append({
                            'name': relative_path,
                            'size_mb': size_mb,
                            'is_video': any(relative_path.lower().endswith(ext) for ext in ['.mp4', '.avi', '.mkv', '.mov'])
                        })
                    else:
                        # Arquivo em subpasta
                        parts = relative_path.split('/')
                        folder = parts[0]
                        filename = parts[-1]
                        
                        if folder not in subfolders:
                            subfolders[folder] = []
                        
                        subfolders[folder].append({
                            'name': filename,
                            'size_mb': size_mb,
                            'is_video': any(filename.lower().endswith(ext) for ext in ['.mp4', '.avi', '.mkv', '.mov'])
                        })
        
        # Mostrar estrutura
        print("🏠 RAIZ (users/sergio_sena/):")
        if root_files:
            for file in root_files:
                icon = "🎬" if file['is_video'] else "📄"
                print(f"   {icon} {file['name']} ({file['size_mb']} MB)")
        else:
            print("   (vazia)")
        
        print()
        
        for folder, files in subfolders.items():
            print(f"📁 {folder}/:")
            for file in files:
                icon = "🎬" if file['is_video'] else "📄"
                print(f"   {icon} {file['name']} ({file['size_mb']} MB)")
            print()
        
        # Verificar SergioSenaTeste.mp4 especificamente
        sergio_test_found = False
        for file in root_files:
            if file['name'] == 'SergioSenaTeste.mp4':
                print(f"✅ SergioSenaTeste.mp4 encontrado na RAIZ ({file['size_mb']} MB)")
                sergio_test_found = True
                break
        
        if not sergio_test_found:
            for folder, files in subfolders.items():
                for file in files:
                    if file['name'] == 'SergioSenaTeste.mp4':
                        print(f"✅ SergioSenaTeste.mp4 encontrado em {folder}/ ({file['size_mb']} MB)")
                        sergio_test_found = True
                        break
        
        if not sergio_test_found:
            print("❌ SergioSenaTeste.mp4 NÃO encontrado")
        
        # Contar vídeos em subpastas
        videos_in_subfolders = 0
        for folder, files in subfolders.items():
            for file in files:
                if file['is_video']:
                    videos_in_subfolders += 1
        
        print(f"\n📊 Resumo:")
        print(f"   Arquivos na raiz: {len(root_files)}")
        print(f"   Subpastas: {len(subfolders)}")
        print(f"   Vídeos em subpastas: {videos_in_subfolders}")
        
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == '__main__':
    check_sergio_structure()