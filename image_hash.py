import zlib
import hashlib
results={}
image_file = open("/home/yousuf/Downloads/exif-samples-master/jpg/Konica_Minolta_DiMAGE_Z3.jpg", 'rb').read()

#image_file = open("/home/yousuf/Downloads/exif-samples-master/jpg/Konica_Minolta_DiMAGE_Z3.jpg").read()
hash_md5=hashlib.md5(image_file).hexdigest()
results["hash_md5"]="'"+hash_md5+"'"
results["hash_sha1"]="'"+hashlib.sha1(image_file).hexdigest()+"'"
results["hash_sha224"]="'"+hashlib.sha224(image_file).hexdigest()+"'"
results["hash_sha256"]="'"+hashlib.sha256(image_file).hexdigest()+"'"
results["hash_sha384"]="'"+hashlib.sha384(image_file).hexdigest()+"'"
results["hash_sha512"]="'"+hashlib.sha512(image_file).hexdigest()+"'"
results["hash_crc32"]="'"+"%08X".lower() % (zlib.crc32(image_file) & 0xFFFFFFFF,)+"'"

#"'"+hashlib.sha1(image_file).hexdigest()+"'"


