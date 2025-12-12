"""
Script kiểm tra cú pháp Python của Remote Control App
Chạy script này để đảm bảo không có lỗi syntax
"""
import ast
import sys
from pathlib import Path

def check_syntax(file_path):
    """Kiểm tra cú pháp Python của một file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        ast.parse(code)
        return True, "OK"
    except SyntaxError as e:
        return False, f"Syntax Error at line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, str(e)

def main():
    # Danh sách files cần kiểm tra
    base_dir = Path(__file__).parent
    files_to_check = [
        base_dir / 'socket_client.py',
        base_dir / 'views.py',
        base_dir / 'urls.py',
        base_dir / 'apps.py',
        base_dir / 'models.py',
        base_dir / 'admin.py',
    ]
    
    print("=" * 60)
    print("REMOTE CONTROL APP - SYNTAX CHECK")
    print("=" * 60)
    
    all_ok = True
    for file_path in files_to_check:
        if file_path.exists():
            ok, msg = check_syntax(file_path)
            status = "✓ PASS" if ok else "✗ FAIL"
            print(f"{status} | {file_path.name:20} | {msg}")
            if not ok:
                all_ok = False
        else:
            print(f"⚠ SKIP | {file_path.name:20} | File not found")
    
    print("=" * 60)
    if all_ok:
        print("✅ All files passed syntax check!")
        return 0
    else:
        print("❌ Some files have syntax errors!")
        return 1

if __name__ == '__main__':
    sys.exit(main())
