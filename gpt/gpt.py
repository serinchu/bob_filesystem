# BoB 7기 보안제품개발 트랙 이세린
# gpt.py
import sys
import struct

def read_sectors(fd, sector, count = 1):
    fd.seek(sector * 512)
    return fd.read(count * 512)
    
def check_GPT(data):
	if data[0] == 0x45 and data[1] == 0x46 and data[2] == 0x49 and data[3] == 0x20 and \
		data[4] == 0x50 and data[5] == 0x41 and data[6] == 0x52 and data[7] == 0x54:
		return 1
	else:
		print("GPT가 아닙니다")
		return -1

print('{:>15}'.format("Partition"),'{:>10}'.format("시작위치"),'{:>5}'.format("사이즈"))

#gpt인지 확인
filename = sys.argv[1]
f = open(filename, "rb")
data = read_sectors(f, 1)
check_GPT(data)

data = read_sectors(f,2,32)
nPartitionNum = 1

for i in list(range(0,128)):
	first_LBA = struct.unpack_from("<L", data, i*0x80 + 32)[0]
	#partition entry가 아닌것 => 그냥 넘어가기
	if first_LBA == 0:
		continue
	last_LBA = struct.unpack_from("<L", data, i*0x80 + 40)[0]
	#size = (last_LBA - first_LBA) * 0x200
	print('{:>15}'.format("Partition"),nPartitionNum,'{:>10}'.format(first_LBA * 0x200),'{:>10}'.format(( last_LBA - first_LBA + 1 ) * 0x200))
	nPartitionNum += 1
	