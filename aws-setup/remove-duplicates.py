#!/usr/bin/env python3
import boto3
from collections import defaultdict

def remove_duplicates():
    """Remove duplicate files, keeping only those in folders"""
    
    s3_client = boto3.client('s3')
    bucket_name = 'mediaflow-uploads-969430605054'
    
    print(f"Scanning for duplicates in: {bucket_name}")
    
    # List all files
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    all_files = response.get('Contents', [])
    
    # Group files by name
    files_by_name = defaultdict(list)
    
    for obj in all_files:
        key = obj['Key']
        filename = key.split('/')[-1]  # Get just the filename
        
        files_by_name[filename].append({
            'key': key,
            'size': obj['Size'],
            'modified': obj['LastModified'],
            'is_root': '/' not in key  # True if file is in root
        })
    
    # Find duplicates and decide what to remove
    to_remove = []
    duplicates_found = 0
    
    for filename, files in files_by_name.items():
        if len(files) > 1:  # Has duplicates
            duplicates_found += 1
            
            # Check if we have both root and folder versions
            root_files = [f for f in files if f['is_root']]
            folder_files = [f for f in files if not f['is_root']]
            
            if root_files and folder_files:
                # Remove root files, keep folder files
                for root_file in root_files:
                    to_remove.append(root_file['key'])
                    print(f"[REMOVE] {root_file['key']} (duplicate in folder)")
    
    print(f"\nFound {duplicates_found} sets of duplicates")
    print(f"Files to remove: {len(to_remove)}")
    
    if not to_remove:
        print("No duplicates to remove!")
        return
    
    # Confirm before deletion
    print(f"\nWill remove {len(to_remove)} root files that have folder duplicates:")
    for key in to_remove[:10]:  # Show first 10
        print(f"  - {key}")
    if len(to_remove) > 10:
        print(f"  ... and {len(to_remove) - 10} more")
    
    confirm = input(f"\nProceed with deletion? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Cancelled.")
        return
    
    # Delete files
    deleted_count = 0
    
    for key in to_remove:
        try:
            s3_client.delete_object(Bucket=bucket_name, Key=key)
            deleted_count += 1
            print(f"[OK] Deleted: {key}")
        except Exception as e:
            print(f"[ERROR] Failed to delete {key}: {str(e)}")
    
    print(f"\n[SUMMARY]")
    print(f"Successfully deleted: {deleted_count}/{len(to_remove)} files")
    print(f"Duplicates cleaned - folder versions preserved!")

if __name__ == "__main__":
    remove_duplicates()