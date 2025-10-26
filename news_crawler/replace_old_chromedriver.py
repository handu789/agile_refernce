import os
import shutil
import zipfile
import stat
import time
import psutil

class ChromeDriverReplacer:
    def __init__(self):
        self.base_dir = r"C:\Program Files\Google\Chrome\Application"
        self.zip_path = os.path.join(self.base_dir, "chromedriver-win64.zip")
        self.old_dir = os.path.join(self.base_dir, "chromedriver-win64")
        self.temp_extract_dir = os.path.join(self.base_dir, "temp_extract")

    def kill_process(self, process_name="chromedriver.exe"):
        print(f"🔍 检查是否存在运行中的 {process_name} 进程")
        found = False
        for proc in psutil.process_iter():
            try:
                if proc.name().lower() == process_name.lower():
                    print(f"🛑 杀死进程 PID {proc.pid}")
                    proc.kill()
                    found = True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        if not found:
            print("✅ 没有运行中的 chromedriver.exe")

    def remove_old_folder(self):
        if os.path.exists(self.old_dir):
            print(f"🧹 删除旧文件夹：{self.old_dir}")
            # 清除只读权限
            for root, dirs, files in os.walk(self.old_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    os.chmod(file_path, stat.S_IWRITE)
            shutil.rmtree(self.old_dir)
            print("✅ 旧版本已删除")
        else:
            print("ℹ️ 未检测到旧文件夹，无需删除")

    def unzip_new_driver(self):
        if not os.path.exists(self.zip_path):
            raise FileNotFoundError(f"❌ 未找到压缩包：{self.zip_path}")
        print(f"📦 解压文件：{self.zip_path}")

        with zipfile.ZipFile(self.zip_path, "r") as zip_ref:
            zip_ref.extractall(self.temp_extract_dir)
        print(f"✅ 解压完成，临时路径：{self.temp_extract_dir}")

    def move_new_folder(self):
        # 查找解压后的文件夹
        subdirs = [d for d in os.listdir(self.temp_extract_dir) if os.path.isdir(os.path.join(self.temp_extract_dir, d))]
        if not subdirs:
            raise RuntimeError("❌ 解压失败，未找到解压后的文件夹")
        extracted_dir = os.path.join(self.temp_extract_dir, subdirs[0])
        shutil.move(extracted_dir, self.old_dir)
        print(f"🚀 已将新版本移动为：{self.old_dir}")
        shutil.rmtree(self.temp_extract_dir)

    def run(self):
        self.kill_process()
        time.sleep(1)
        self.remove_old_folder()
        time.sleep(1)
        self.unzip_new_driver()
        self.move_new_folder()
        print("🎉 ChromeDriver 更新完成！")

if __name__ == "__main__":
    updater = ChromeDriverReplacer()
    updater.run()
