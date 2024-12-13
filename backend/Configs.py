# Configs.py
import sys
import re

class Config:
    class Email:
        Account = "1023044626@qq.com"
        Password = "fevsouzjombtbdgi"

    class API:
        Version = "v0.1.7"
        AppName = "DjangoRestfulAPI"
        FileName = "DjangoRestfulAPI"
        CompanyName = "Guest Liang"
        LegalCopyright = "2024 © Guest Liang"
        ProductName = "GuestLiang Django Restful API"

    class Electron:
        Name = "guestliang-electron-app"
        Version = "0.2.5" # Same as package.json


def update_api_version(increment_type="patch"):
    try: 
        with open(__file__, "r", encoding="utf-8") as f:
            content = f.read()

        # 匹配API版本号 vX.X.X 格式 (捕获数字部分)
        pattern = r'(Version\s*=\s*"v)(\d+\.\d+\.\d+)(")'
        match = re.search(pattern, content)
        if match:
            old_version = match.group(2)
            parts = old_version.split(".")

            # 根据increment_type决定如何递增版本
            if increment_type == "major":
                parts[0] = str(int(parts[0]) + 1)
                parts[1] = "0"
                parts[2] = "0"
            elif increment_type == "minor":
                parts[1] = str(int(parts[1]) + 1)
                parts[2] = "0"
            else:  # 默认patch
                parts[2] = str(int(parts[2]) + 1)

            new_version = ".".join(parts)
            new_content = content[:match.start(2)] + new_version + content[match.end(2):]

            with open(__file__, "w", encoding="utf-8") as f:
                f.write(new_content)
    except Exception as e:
        print(f"Failed to update API version: {e}")


def update_electron_version(increment_type="patch"):
    try: 
        with open(__file__, "r", encoding="utf-8") as f:
            content = f.read()

        # 匹配Electron版本号 X.X.X 格式
        pattern = r'(Version\s*=\s*")(\d+\.\d+\.\d+)(")'
        match = re.search(pattern, content)
        if match:
            old_version = match.group(2)
            parts = old_version.split(".")

            # 根据increment_type决定如何递增版本
            if increment_type == "major":
                parts[0] = str(int(parts[0]) + 1)
                parts[1] = "0"
                parts[2] = "0"
            elif increment_type == "minor":
                parts[1] = str(int(parts[1]) + 1)
                parts[2] = "0"
            else:  # 默认patch
                parts[2] = str(int(parts[2]) + 1)

            new_version = ".".join(parts)
            new_content = content[:match.start(2)] + new_version + content[match.end(2):]

            with open(__file__, "w", encoding="utf-8") as f:
                f.write(new_content)
    except Exception as e:
        print(f"Failed to update Electron version: {e}")

def update_frontend_version():
    try:
        import json
        import os

        frontend_package_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "package.json")

        with open(frontend_package_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        data["version"] = Config.Electron.Version

        with open(frontend_package_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"package.json version has updated to {Config.Electron.Version}")
    except Exception as e:
        print(f"Failed to sync package.json version: {e}")



if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("未提供任何参数，请使用 \n    --api-major / --api-minor / --api-patch 更新api版本号 \n 或 --electron-major / --electron-minor / --electron-patch 更新electron版本号 \n 或 --sync-packagejson 同步package.json版本号")
        sys.exit(1)

    updated = False

    if "--api-major" in sys.argv:
        update_api_version("major")
        updated = True
    elif "--api-minor" in sys.argv:
        update_api_version("minor")
        updated = True
    elif "--api-patch" in sys.argv:
        update_api_version("patch")
        updated = True

    if "--electron-major" in sys.argv:
        update_electron_version("major")
        updated = True
    elif "--electron-minor" in sys.argv:
        update_electron_version("minor")
        updated = True
    elif "--electron-patch" in sys.argv:
        update_electron_version("patch")
        updated = True

    if "--sync-packagejson" in sys.argv:
        update_frontend_version()
        updated = True

    if not updated:
        print("未定义的参数，请使用 \n    --api-major / --api-minor / --api-patch 更新api版本号 \n 或 --electron-major / --electron-minor / --electron-patch 更新electron版本号 \n 或 --sync-packagejson 同步package.json版本号")
        sys.exit(1)