import hashlib
import os


def QA_util_file_md5(filename):
    
    """
    explanation:
        获取文件的MD5值		

    params:
        * filename ->:
            meaning: 文件路径
            type: null
            optional: [null]

    return:
        str
	
    demonstrate:
        Not described
	
    output:
        Not described
    """

    with open(filename, mode='rb') as f:
        d = hashlib.md5()
        while True:
            # 128 is smaller than the typical filesystem block
            buf = f.read(4096)
            if not buf:
                break
            d.update(buf)
        return d.hexdigest()


def QA_util_file_size(filename):
    return os.path.getsize(file)
