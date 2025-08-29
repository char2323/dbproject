import os


def is_binary_file(file_path, blocksize=512):
    """判断文件是否为二进制文件"""
    try:
        with open(file_path, "rb") as f:
            block = f.read(blocksize)
            if b"\0" in block:  # 含有空字节基本是二进制文件
                return True
        return False
    except Exception:
        return True  # 出错时当成二进制文件


def collect_files(root_dir, output_file="output.txt"):
    with open(output_file, "w", encoding="utf-8") as out:
        for foldername, _, filenames in os.walk(root_dir):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                if is_binary_file(file_path):
                    continue  # 跳过二进制文件

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                except Exception:
                    # 如果不是 utf-8，可以尝试 gbk
                    try:
                        with open(file_path, "r", encoding="gbk") as f:
                            content = f.read()
                    except Exception:
                        continue  # 还是不行就跳过

                # 写入输出文件
                out.write(f"=== 文件: {file_path} ===\n")
                out.write(content + "\n\n")

    print(f"✅ 已完成，输出保存到 {output_file}")


if __name__ == "__main__":
    folder = input("请输入要扫描的文件夹路径: ").strip()
    collect_files(folder, "output.txt")
