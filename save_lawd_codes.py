import csv
import sys
import os

# Windows 터미널 한글 출력 처리
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# ==============================================================================
# 서울특별시 및 경기도 법정동 시군구 코드 (LAWD_CD 5자리) 데이터
# ==============================================================================

SEOUL_LAWD_CODES = [
    {"sido": "서울특별시", "sgg_nm": "종로구", "lawd_cd": "11110"},
    {"sido": "서울특별시", "sgg_nm": "중구", "lawd_cd": "11140"},
    {"sido": "서울특별시", "sgg_nm": "용산구", "lawd_cd": "11170"},
    {"sido": "서울특별시", "sgg_nm": "성동구", "lawd_cd": "11200"},
    {"sido": "서울특별시", "sgg_nm": "광진구", "lawd_cd": "11215"},
    {"sido": "서울특별시", "sgg_nm": "동대문구", "lawd_cd": "11230"},
    {"sido": "서울특별시", "sgg_nm": "중랑구", "lawd_cd": "11260"},
    {"sido": "서울특별시", "sgg_nm": "성북구", "lawd_cd": "11290"},
    {"sido": "서울특별시", "sgg_nm": "강북구", "lawd_cd": "11305"},
    {"sido": "서울특별시", "sgg_nm": "도봉구", "lawd_cd": "11320"},
    {"sido": "서울특별시", "sgg_nm": "노원구", "lawd_cd": "11350"},
    {"sido": "서울특별시", "sgg_nm": "은평구", "lawd_cd": "11380"},
    {"sido": "서울특별시", "sgg_nm": "서대문구", "lawd_cd": "11410"},
    {"sido": "서울특별시", "sgg_nm": "마포구", "lawd_cd": "11440"},
    {"sido": "서울특별시", "sgg_nm": "양천구", "lawd_cd": "11470"},
    {"sido": "서울특별시", "sgg_nm": "강서구", "lawd_cd": "11500"},
    {"sido": "서울특별시", "sgg_nm": "구로구", "lawd_cd": "11530"},
    {"sido": "서울특별시", "sgg_nm": "금천구", "lawd_cd": "11545"},
    {"sido": "서울특별시", "sgg_nm": "영등포구", "lawd_cd": "11560"},
    {"sido": "서울특별시", "sgg_nm": "동작구", "lawd_cd": "11590"},
    {"sido": "서울특별시", "sgg_nm": "관악구", "lawd_cd": "11620"},
    {"sido": "서울특별시", "sgg_nm": "서초구", "lawd_cd": "11650"},
    {"sido": "서울특별시", "sgg_nm": "강남구", "lawd_cd": "11680"},
    {"sido": "서울특별시", "sgg_nm": "송파구", "lawd_cd": "11710"},
    {"sido": "서울특별시", "sgg_nm": "강동구", "lawd_cd": "11740"}
]

GYEONGGI_LAWD_CODES = [
    # 수원시
    {"sido": "경기도", "sgg_nm": "수원시 장안구", "lawd_cd": "41111"},
    {"sido": "경기도", "sgg_nm": "수원시 권선구", "lawd_cd": "41113"},
    {"sido": "경기도", "sgg_nm": "수원시 팔달구", "lawd_cd": "41115"},
    {"sido": "경기도", "sgg_nm": "수원시 영통구", "lawd_cd": "41117"},
    
    # 성남시
    {"sido": "경기도", "sgg_nm": "성남시 수정구", "lawd_cd": "41131"},
    {"sido": "경기도", "sgg_nm": "성남시 중원구", "lawd_cd": "41133"},
    {"sido": "경기도", "sgg_nm": "성남시 분당구", "lawd_cd": "41135"},
    
    # 의정부시
    {"sido": "경기도", "sgg_nm": "의정부시", "lawd_cd": "41150"},
    
    # 안양시
    {"sido": "경기도", "sgg_nm": "안양시 만안구", "lawd_cd": "41171"},
    {"sido": "경기도", "sgg_nm": "안양시 동안구", "lawd_cd": "41173"},
    
    # 부천시
    {"sido": "경기도", "sgg_nm": "부천시 원미구", "lawd_cd": "41192"},
    {"sido": "경기도", "sgg_nm": "부천시 소사구", "lawd_cd": "41194"},
    {"sido": "경기도", "sgg_nm": "부천시 오정구", "lawd_cd": "41196"},
    
    # 광명시, 평택시, 동두천시
    {"sido": "경기도", "sgg_nm": "광명시", "lawd_cd": "41210"},
    {"sido": "경기도", "sgg_nm": "평택시", "lawd_cd": "41220"},
    {"sido": "경기도", "sgg_nm": "동두천시", "lawd_cd": "41250"},
    
    # 안산시
    {"sido": "경기도", "sgg_nm": "안산시 상록구", "lawd_cd": "41271"},
    {"sido": "경기도", "sgg_nm": "안산시 단원구", "lawd_cd": "41273"},
    
    # 고양시
    {"sido": "경기도", "sgg_nm": "고양시 덕양구", "lawd_cd": "41281"},
    {"sido": "경기도", "sgg_nm": "고양시 일산동구", "lawd_cd": "41285"},
    {"sido": "경기도", "sgg_nm": "고양시 일산서구", "lawd_cd": "41287"},
    
    # 과천시, 구리시, 남양주시, 오산시, 시흥시, 군포시, 의왕시, 하남시
    {"sido": "경기도", "sgg_nm": "과천시", "lawd_cd": "41290"},
    {"sido": "경기도", "sgg_nm": "구리시", "lawd_cd": "41310"},
    {"sido": "경기도", "sgg_nm": "남양주시", "lawd_cd": "41360"},
    {"sido": "경기도", "sgg_nm": "오산시", "lawd_cd": "41370"},
    {"sido": "경기도", "sgg_nm": "시흥시", "lawd_cd": "41390"},
    {"sido": "경기도", "sgg_nm": "군포시", "lawd_cd": "41410"},
    {"sido": "경기도", "sgg_nm": "의왕시", "lawd_cd": "41430"},
    {"sido": "경기도", "sgg_nm": "하남시", "lawd_cd": "41450"},
    
    # 용인시
    {"sido": "경기도", "sgg_nm": "용인시 처인구", "lawd_cd": "41461"},
    {"sido": "경기도", "sgg_nm": "용인시 기흥구", "lawd_cd": "41463"},
    {"sido": "경기도", "sgg_nm": "용인시 수지구", "lawd_cd": "41465"},
    
    # 파주시, 이천시, 안성시, 김포시, 화성시, 광주시, 양주시, 포천시, 여주시
    {"sido": "경기도", "sgg_nm": "파주시", "lawd_cd": "41480"},
    {"sido": "경기도", "sgg_nm": "이천시", "lawd_cd": "41500"},
    {"sido": "경기도", "sgg_nm": "안성시", "lawd_cd": "41550"},
    {"sido": "경기도", "sgg_nm": "김포시", "lawd_cd": "41570"},
    {"sido": "경기도", "sgg_nm": "화성시", "lawd_cd": "41590"},
    {"sido": "경기도", "sgg_nm": "광주시", "lawd_cd": "41610"},
    {"sido": "경기도", "sgg_nm": "양주시", "lawd_cd": "41630"},
    {"sido": "경기도", "sgg_nm": "포천시", "lawd_cd": "41650"},
    {"sido": "경기도", "sgg_nm": "여주시", "lawd_cd": "41670"},
    
    # 군 단위
    {"sido": "경기도", "sgg_nm": "연천군", "lawd_cd": "41800"},
    {"sido": "경기도", "sgg_nm": "가평군", "lawd_cd": "41820"},
    {"sido": "경기도", "sgg_nm": "양평군", "lawd_cd": "41830"}
]


def generate_lawd_csv(output_file="seoul_gyeonggi_lawd_codes.csv"):
    all_codes = SEOUL_LAWD_CODES + GYEONGGI_LAWD_CODES

    # full_name 추가
    for item in all_codes:
        item["full_name"] = f"{item['sido']} {item['sgg_nm']}"

    fieldnames = ["sido", "sgg_nm", "lawd_cd", "full_name"]

    print(f"📄 서울/경기 지역코드 CSV 생성 시작: '{output_file}'")

    try:
        # utf-8-sig 로 저장하여 Excel에서도 한글 깨짐 없이 바로 열릴 수 있도록 함
        with open(output_file, mode="w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_codes)

        seoul_count = len(SEOUL_LAWD_CODES)
        gyeonggi_count = len(GYEONGGI_LAWD_CODES)
        total_count = len(all_codes)

        print("=" * 60)
        print(f"✅ CSV 파일 생성 성공! ({os.path.abspath(output_file)})")
        print(f"   - 서울특별시 자치구: {seoul_count}개")
        print(f"   - 경기도 시군구:     {gyeonggi_count}개")
        print(f"   - 총 지역코드 개수:  {total_count}개")
        print("=" * 60)

    except Exception as e:
        print(f"❌ CSV 저장 중 오류 발생: {e}")


if __name__ == "__main__":
    output_filename = "seoul_gyeonggi_lawd_codes.csv"
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]

    generate_lawd_csv(output_filename)
