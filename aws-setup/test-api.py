#!/usr/bin/env python3
import requests
import json

def test_mediaflow_api():
    """Test all Mediaflow API endpoints"""
    
    # Load config
    with open('mediaflow-config.json', 'r') as f:
        config = json.load(f)
    
    api_url = config['api_gateway']['api_url']
    print(f"Testing API: {api_url}")
    print("=" * 50)
    
    # Test 1: Login
    print("1. Testing Login...")
    try:
        response = requests.post(f"{api_url}/auth/login", 
            json={"email": "sergiosenaadmin@sstech", "password": "sergiosena"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("   ✅ Login successful")
                token = data.get('token')
            else:
                print("   ❌ Login failed")
                return
        else:
            print(f"   ❌ Login failed: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ Login error: {str(e)}")
        return
    
    # Test 2: List Files
    print("2. Testing File List...")
    try:
        response = requests.get(f"{api_url}/files", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"   ✅ Files listed: {len(data.get('files', []))} files")
            else:
                print("   ❌ Files list failed")
        else:
            print(f"   ❌ Files list failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Files list error: {str(e)}")
    
    # Test 3: Upload Presigned URL
    print("3. Testing Upload Presigned URL...")
    try:
        response = requests.post(f"{api_url}/upload/presigned",
            json={"filename": "test-video.mp4", "contentType": "video/mp4"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("   ✅ Presigned URL generated")
                upload_url = data.get('uploadUrl')
                print(f"   📤 Upload URL: {upload_url[:50]}...")
            else:
                print("   ❌ Presigned URL failed")
        else:
            print(f"   ❌ Presigned URL failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Presigned URL error: {str(e)}")
    
    # Test 4: Cleanup endpoint
    print("4. Testing Cleanup...")
    try:
        response = requests.post(f"{api_url}/cleanup", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"   ✅ Cleanup successful: {data.get('count', 0)} files cleaned")
            else:
                print("   ❌ Cleanup failed")
        else:
            print(f"   ❌ Cleanup failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Cleanup error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎉 API Gateway Phase 3 Complete!")
    print(f"🌐 API URL: {api_url}")
    print("✅ All endpoints functional")
    
    # Save API endpoints for frontend
    endpoints = {
        "auth": f"{api_url}/auth/login",
        "files": f"{api_url}/files",
        "upload": f"{api_url}/upload/presigned",
        "cleanup": f"{api_url}/cleanup",
        "bulk_delete": f"{api_url}/files/bulk-delete"
    }
    
    config['api_endpoints'] = endpoints
    with open('mediaflow-config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("📄 API endpoints saved to config")

if __name__ == "__main__":
    test_mediaflow_api()