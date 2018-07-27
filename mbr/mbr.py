# BoB 7기 보안제품개발 트랙 이세린
# mbr.py
import sys
import struct

def read_sectors(fd, sector, count = 1):
    fd.seek(sector * 512)
    return fd.read(count * 512)
    
def check_boot_record(data):
    if data[-2] != 0x55 and data[-1] != 0xAA:
            print("이 파티션은 Boot Record가 아닙니다.")
            return -1
   
filename = sys.argv[1]
f = open(filename, "rb")
data = read_sectors(f, 0)
check_boot_record(data)
partition_data = data[446:446+64]

i=1			#partition number
offset=0	#ebr에서 파티션을 찾아갈 때 쓰는 오프셋
next=0		#ebr에서 다음 ebr 넘어갈 때 쓰는 오프셋
print('{:>15}'.format("Partition"),'{:>10}'.format("시작위치"),'{:>5}'.format("사이즈"))

while True:

	table = partition_data[:16]
	partition_data = partition_data[16:]
	
	if struct.unpack_from("<I", table, 8)[0] == 0:	#더이상 갈 주소가 없다는 것 == ebr 끝
			break	
			
	if offset == 0:									#mbr
		if len(partition_data) == 0:				#mbr의 마지막 파티션 테이블 엔트리
			data = read_sectors(f,struct.unpack_from("<I", table, 8)[0])   			#다음 ebr로 넘어가자
			check_boot_record(data)                        							#부트 레코드인지 확인, 아니면 종료
			partition_data = data[446:446+32]		#어차피 ebr은 2 엔트리
			offset = struct.unpack_from("<I", table, 8)[0]
			
		else:
			print('{:>15}'.format("Partition"),i,'{:>10}'.format((struct.unpack_from("<I", table, 8)[0]) * 512),'{:>10}'.format(struct.unpack_from("<I", table, 12)[0]))   
			i+=1
			
	else:											#ebr
		if len(partition_data) == 0:				#ebr의 마지막 파티션 테이블 엔트리
			next = struct.unpack_from("<I", table, 8)[0]
			data = read_sectors(f,offset + struct.unpack_from("<I", table, 8)[0])    #다음 ebr로 넘어가자
			check_boot_record(data)                       	 						 #부트 레코드인지 확인, 아니면 종료
			partition_data = data[446:446+32]
		else:
			print('{:>15}'.format("Partition"),i,'{:>10}'.format((offset + next + struct.unpack_from("<I", table, 8)[0]) * 512),'{:>10}'.format(struct.unpack_from("<I", table, 12)[0])) 
			i+=1