#!/usr/bin/env python3
import boto3

def replace_converted_files():
    """Replace original .ts files with their converted .mp4 versions"""
    
    s3_client = boto3.client('s3')
    bucket_name = 'mediaflow-uploads-969430605054'
    
    print(f"Scanning for converted files in: {bucket_name}")
    
    # List all files
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    all_files = response.get('Contents', [])
    
    replacements = []
    
    for obj in all_files:
        key = obj['Key']
        
        # Look for converted MP4 files with weird names
        if '.mp4' in key and ('converted' in key or key.count('.mp4') > 1 or '...' in key):
            # Try to find the original .ts file
            possible_original = None
            
            # Extract base name and try different patterns
            if 'converted' in key:
                possible_original = key.replace('converted.mp4', '.ts')
            elif key.count('.mp4') > 1:
                # Handle duplicated .mp4 extensions
                base_name = key.split('.mp4')[0]
                possible_original = f"{base_name}.ts"
            elif '...' in key:
                # Handle truncated names
                base_parts = key.split('...')
                if len(base_parts) >= 2:
                    base_name = base_parts[0]
                    possible_original = f"{base_name}.ts"
            
            if possible_original:
                # Check if original exists
                try:
                    s3_client.head_object(Bucket=bucket_name, Key=possible_original)
                    replacements.append({
                        'converted': key,
                        'original': possible_original,
                        'target': possible_original.replace('.ts', '.mp4')
                    })
                    print(f"Found pair: {possible_original} -> {key}")
                except:
                    # Original doesn't exist, skip
                    pass
    
    print(f"\nFound {len(replacements)} files to replace:")
    for r in replacements:
        print(f"  {r['original']} -> {r['target']} (using {r['converted']})")
    
    if not replacements:
        print("No files to replace!")
        return
    
    confirm = input(f"\nProceed with {len(replacements)} replacements? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Cancelled.")
        return
    
    # Perform replacements
    success_count = 0
    
    for r in replacements:
        try:
            # Copy converted file to replace original (with .mp4 extension)
            s3_client.copy_object(
                Bucket=bucket_name,
                CopySource={'Bucket': bucket_name, 'Key': r['converted']},
                Key=r['target']
            )
            
            # Delete original .ts file
            s3_client.delete_object(Bucket=bucket_name, Key=r['original'])
            
            # Delete converted file (if different from target)
            if r['converted'] != r['target']:
                s3_client.delete_object(Bucket=bucket_name, Key=r['converted'])
            
            print(f"[OK] Replaced {r['original']} with {r['target']}")
            success_count += 1
            
        except Exception as e:
            print(f"[ERROR] Failed to replace {r['original']}: {str(e)}")
    
    print(f"\n[SUMMARY]")
    print(f"Successfully replaced: {success_count}/{len(replacements)} files")
    print(f"Converted files now replace originals with .mp4 extension!")

if __name__ == "__main__":
    replace_converted_files()