import urllib.request
import urllib.parse
import urllib.error
import json
import xml.etree.ElementTree as ET
import sys
import os
import csv
import argparse

# ==============================================================================
# 기본 설정 정보
# ==============================================================================
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

DATA_GO_URL = "https://apis.data.go.kr/1613000/RTMSDataSvcAptTrade/getRTMSDataSvcAptTrade"
SERVICE_KEY = "858b914a7b678bf5f8b474d348f703840f333e1d322b8918c217303444e2619e"

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://fxjtykeuznhnyctyqalc.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")
TABLE_NAME = "apartment_deals"

DEFAULT_LAWD_CD = "41135"  # 성남시 분당구
DEFAULT_DEAL_YMD = "202405"
DEFAULT_CSV_FILE = "seoul_gyeonggi_lawd_codes.csv"


def generate_ymd_list(ymd_input, start_ymd_input=None, end_ymd_input=None):
    """
    단일 월('202405') 또는 기간 범위('202401-202607', '2024.01~2026.07')에 해당하는 YYYYMM 연월 리스트를 생성합니다.
    """
    def make_range(s_ymd, e_ymd):
        try:
            start_y, start_m = int(s_ymd[:4]), int(s_ymd[4:6])
            end_y, end_m = int(e_ymd[:4]), int(e_ymd[4:6])
        except Exception:
            print(f"❌ 날짜 형식이 잘못되었습니다: {s_ymd} ~ {e_ymd}")
            return []

        ymd_list = []
        curr_y, curr_m = start_y, start_m

        while (curr_y < end_y) or (curr_y == end_y and curr_m <= end_m):
            ymd_list.append(f"{curr_y}{curr_m:02d}")
            curr_m += 1
            if curr_m > 12:
                curr_m = 1
                curr_y += 1

        return ymd_list

    # 1. --start-ymd 및 --end-ymd 가 제공된 경우
    if start_ymd_input and end_ymd_input:
        s_str = str(start_ymd_input).replace('.', '').replace('-', '').strip()
        e_str = str(end_ymd_input).replace('.', '').replace('-', '').strip()
        return make_range(s_str, e_str)

    # 2. --ymd 파라미터 내 범위 구분자 ('-', '~', ':')가 있는 경우
    clean_input = str(ymd_input).replace(' ', '')
    for sep in ['~', ':', '-']:
        if sep in clean_input:
            parts = clean_input.split(sep)
            if len(parts) == 2:
                s_str = parts[0].replace('.', '').strip()
                e_str = parts[1].replace('.', '').strip()
                return make_range(s_str, e_str)

    # 3. 단일 월인 경우
    single_clean = clean_input.replace('.', '').strip()
    return [single_clean]


def fetch_rtms_data(lawd_cd, deal_ymd, region_name="", num_of_rows=1000):
    """
    국토교통부 아파트 매매 실거래가 Open API 데이터를 조회합니다.
    """
    display_name = f"{region_name} ({lawd_cd})" if region_name else lawd_cd
    print(f"📡 [API 수집중] 지역: {display_name}, 계약월: {deal_ymd}...")

    params = {
        "serviceKey": SERVICE_KEY,
        "LAWD_CD": lawd_cd,
        "DEAL_YMD": deal_ymd,
        "numOfRows": str(num_of_rows),
        "_type": "json"
    }

    query_string = urllib.parse.urlencode(params, safe='')
    full_url = f"{DATA_GO_URL}?{query_string}"

    req = urllib.request.Request(full_url)

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read().decode('utf-8')
            
            try:
                data = json.loads(content)
                body = data.get("response", {}).get("body", {})
                items = body.get("items", {})
                
                if isinstance(items, dict) and "item" in items:
                    item_list = items["item"]
                    if isinstance(item_list, dict):
                        item_list = [item_list]
                    print(f"  └ ✅ API {len(item_list)}건 수집 완료")
                    return item_list
                elif isinstance(items, list):
                    print(f"  └ ✅ API {len(items)}건 수집 완료")
                    return items
                else:
                    print("  └ ℹ️ 수집된 실거래가 데이터가 없습니다.")
                    return []
            except json.JSONDecodeError:
                return parse_xml_items(content)

    except Exception as e:
        print(f"  └ ❌ API 수집 실패: {e}")
        return []


def parse_xml_items(xml_content):
    """XML 응답 결과를 파싱하여 dict 리스트로 변환합니다."""
    items = []
    try:
        root = ET.fromstring(xml_content)
        for item_node in root.findall(".//item"):
            row = {}
            for child in item_node:
                row[child.tag] = child.text.strip() if child.text else ""
            items.append(row)
        print(f"  └ ✅ XML {len(items)}건 수집 완료")
    except Exception as e:
        print(f"  └ ❌ XML 파싱 에러: {e}")
    return items


def clean_record(item):
    """
    공공데이터 API의 결과를 Supabase apartment_deals 테이블 스키마에 맞게 정제합니다.
    """
    def to_int(val):
        try:
            return int(str(val).replace(',', '').strip())
        except (ValueError, TypeError):
            return None

    def to_float(val):
        try:
            return float(str(val).replace(',', '').strip())
        except (ValueError, TypeError):
            return None

    def to_str(val):
        if val is None:
            return ""
        return str(val).strip()

    return {
        "aptDong": to_str(item.get("aptDong")),
        "aptNm": to_str(item.get("aptNm")),
        "buildYear": to_int(item.get("buildYear")),
        "buyerGbn": to_str(item.get("buyerGbn")),
        "cdealDay": to_str(item.get("cdealDay")),
        "cdealType": to_str(item.get("cdealType")),
        "dealAmount": to_str(item.get("dealAmount")),
        "dealDay": to_int(item.get("dealDay")),
        "dealMonth": to_int(item.get("dealMonth")),
        "dealYear": to_int(item.get("dealYear")),
        "dealingGbn": to_str(item.get("dealingGbn")),
        "estateAgentSggNm": to_str(item.get("estateAgentSggNm")),
        "excluUseAr": to_float(item.get("excluUseAr")),
        "floor": to_int(item.get("floor")),
        "jibun": to_str(item.get("jibun")),
        "landLeaseholdGbn": to_str(item.get("landLeaseholdGbn")),
        "rgstDate": to_str(item.get("rgstDate")),
        "sggCd": to_str(item.get("sggCd")),
        "slerGbn": to_str(item.get("slerGbn")),
        "umdNm": to_str(item.get("umdNm"))
    }


def get_record_signature(r):
    """실거래가 데이터를 유일하게 식별하기 위한 고유 튜플 서명 생성"""
    return (
        str(r.get("sggCd") or "").strip(),
        str(r.get("umdNm") or "").strip(),
        str(r.get("aptNm") or "").strip(),
        str(r.get("jibun") or "").strip(),
        str(r.get("aptDong") or "").strip(),
        r.get("dealYear"),
        r.get("dealMonth"),
        r.get("dealDay"),
        r.get("floor"),
        r.get("excluUseAr"),
        str(r.get("dealAmount") or "").strip()
    )


def deduplicate_records(records):
    """
    동일한 실거래가 데이터의 중복 건을 메모리 상에서 1차적으로 제거합니다.
    """
    seen = set()
    unique_records = []

    for r in records:
        signature = get_record_signature(r)
        if signature not in seen:
            seen.add(signature)
            unique_records.append(r)

    filtered_count = len(records) - len(unique_records)
    if filtered_count > 0:
        print(f"  └ 🧹 [메모리 중복 제거] {filtered_count}건 중복 제거 (고유: {len(unique_records)}건)")

    return unique_records


def fetch_existing_db_signatures(lawd_cd, deal_ymd, supabase_url, supabase_key, table_name):
    """
    Supabase DB에서 해당 지역코드(sggCd)와 계약월(dealYear, dealMonth)에 이미 존재하는 데이터의 고유 서명 목록을 조회합니다.
    """
    if not lawd_cd or not deal_ymd or len(deal_ymd) < 6:
        return set()

    try:
        year = int(deal_ymd[:4])
        month = int(deal_ymd[4:6])
    except ValueError:
        return set()

    query_params = urllib.parse.urlencode({
        "sggCd": f"eq.{lawd_cd}",
        "dealYear": f"eq.{year}",
        "dealMonth": f"eq.{month}",
        "select": "sggCd,umdNm,aptNm,jibun,aptDong,dealYear,dealMonth,dealDay,floor,excluUseAr,dealAmount"
    })

    endpoint_url = f"{supabase_url.rstrip('/')}/rest/v1/{table_name}?{query_params}"
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}"
    }

    signatures = set()
    from_offset = 0
    step = 1000
    has_more = True

    while has_more:
        req = urllib.request.Request(
            f"{endpoint_url}&limit={step}&offset={from_offset}", 
            headers=headers
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                if data and isinstance(data, list):
                    for r in data:
                        signatures.add(get_record_signature(r))
                    from_offset += step
                    if len(data) < step:
                        has_more = False
                else:
                    has_more = False
        except Exception:
            has_more = False

    return signatures


def upload_to_supabase(records, supabase_url, supabase_key, table_name, resolution="merge-duplicates", batch_size=50):
    """
    정제된 데이터를 Supabase REST API를 통해 업로드(POST)합니다.
    """
    if not records:
        return 0

    endpoint_url = f"{supabase_url.rstrip('/')}/rest/v1/{table_name}"
    
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json",
        "Prefer": f"resolution={resolution},return=representation"
    }

    total_inserted = 0
    total_batches = (len(records) + batch_size - 1) // batch_size

    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]
        batch_num = (i // batch_size) + 1

        json_data = json.dumps(batch, ensure_ascii=False).encode('utf-8')
        req = urllib.request.Request(endpoint_url, data=json_data, headers=headers, method='POST')

        try:
            with urllib.request.urlopen(req) as resp:
                resp_body = resp.read().decode('utf-8')
                inserted_rows = json.loads(resp_body) if resp_body else []
                count = len(inserted_rows) if isinstance(inserted_rows, list) else len(batch)
                total_inserted += count
                print(f"    └ Supabase Batch {batch_num}/{total_batches}: 신규 {count}건 저장 성공")
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode('utf-8')
            
            if e.code == 409 or "23505" in err_msg or "duplicate key" in err_msg.lower():
                print(f"  ⚠️ [DB 중복 감지] Batch {batch_num}: 중복 레코드 제외 처리 중...")
                success_count = upload_single_items_fallback(batch, endpoint_url, headers)
                total_inserted += success_count
            elif e.code == 401 or "row-level security" in err_msg.lower():
                print(f"  ❌ [Supabase 전송 실패] HTTP {e.code}: {err_msg}")
                print("\n" + "="*70)
                print("💡 [RLS 권한 안내]")
                print("Supabase의 'apartment_deals' 테이블에 Row Level Security (RLS) 정책이 설정되어 있습니다.")
                print("데이터를 INSERT 하려면 Supabase 대시보드에서 'Enable insert for anon users' 정책을 추가하거나,")
                print("--key 옵션으로 'service_role key' (Secret Key)를 전달하여 실행하세요.")
                print("="*70 + "\n")
                return -1
            else:
                print(f"  ❌ [Supabase 전송 실패] HTTP {e.code}: {err_msg}")
        except Exception as e:
            print(f"  ❌ [업로드 예외] {e}")

    return total_inserted


def upload_single_items_fallback(batch, endpoint_url, headers):
    """
    배치 전송 시 중복 에러가 발생한 경우, 1건씩 개별 전송하여 중복되지 않은 신규 건만 업로드합니다.
    """
    success_count = 0
    duplicate_count = 0

    for item in batch:
        json_data = json.dumps([item], ensure_ascii=False).encode('utf-8')
        req = urllib.request.Request(endpoint_url, data=json_data, headers=headers, method='POST')

        try:
            with urllib.request.urlopen(req) as resp:
                success_count += 1
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode('utf-8')
            if e.code == 409 or "23505" in err_msg or "duplicate key" in err_msg.lower():
                duplicate_count += 1
            else:
                pass
        except Exception:
            pass

    print(f"    └ 🔄 [개별 수습 완료] 신규 저장: {success_count}건 / 중복 제외: {duplicate_count}건")
    return success_count


def read_lawd_codes_from_csv(csv_path):
    """CSV 파일에서 lawd_cd 목록을 읽어옵니다."""
    regions = []
    if not os.path.exists(csv_path):
        print(f"❌ CSV 파일을 찾을 수 없습니다: {csv_path}")
        return regions

    try:
        with open(csv_path, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                lawd_cd = row.get("lawd_cd", "").strip()
                sido = row.get("sido", "").strip()
                sgg_nm = row.get("sgg_nm", "").strip()
                full_name = row.get("full_name", f"{sido} {sgg_nm}").strip()
                if lawd_cd:
                    regions.append({
                        "lawd_cd": lawd_cd,
                        "full_name": full_name
                    })
        print(f"📄 CSV 파일({os.path.basename(csv_path)})에서 총 {len(regions)}개 지역코드를 로드했습니다.")
    except Exception as e:
        print(f"❌ CSV 파싱 중 에러 발생: {e}")

    return regions


def main():
    parser = argparse.ArgumentParser(description="국토교통부 아파트 실거래가 -> Supabase 수집 스크립트")
    parser.add_argument("--csv", type=str, default="", help="지역코드 CSV 파일 경로 (예: seoul_gyeonggi_lawd_codes.csv)")
    parser.add_argument("--lawd", type=str, default="", help="단일 지역코드 (예: 41135 성남시 분당구, 11680 강남구)")
    parser.add_argument("--ymd", type=str, default=DEFAULT_DEAL_YMD, help="계약월 또는 계약월 기간 범위 (예: 202405 또는 202401-202607, 2024.01~2026.07)")
    parser.add_argument("--start-ymd", type=str, default="", help="시작 계약월 (예: 202401)")
    parser.add_argument("--end-ymd", type=str, default="", help="종료 계약월 (예: 202607)")
    parser.add_argument("--key", type=str, default=SUPABASE_KEY, help="Supabase API Key (service_role 키 사용 권장)")
    parser.add_argument("--on-conflict", type=str, default="merge-duplicates", choices=["merge-duplicates", "ignore-duplicates"],
                        help="중복 데이터 처리 방식 (merge-duplicates: 덮어쓰기/Upsert, ignore-duplicates: 중복 건너뛰기)")

    args = parser.parse_args()

    # 연월(YYYYMM) 범위 생성
    ymd_list = generate_ymd_list(args.ymd, start_ymd_input=args.start_ymd, end_ymd_input=args.end_ymd)

    print("=" * 70)
    print("🏠 국토교통부 아파트 실거래가 수집 & Supabase 업로드 스크립트")
    print(f"📅 대상 계약월 기간: {ymd_list[0]} ~ {ymd_list[-1]} (총 {len(ymd_list)}개월)")
    print(f"⚙️ 중복 데이터 검증: DB 사전 대조 + 메모리 중복 검사 적용")
    print("=" * 70)

    regions_to_process = []

    # 1. 대상 지역 목록 설정
    if args.lawd:
        regions_to_process = [{"lawd_cd": args.lawd, "full_name": args.lawd}]
    else:
        csv_file = args.csv if args.csv else DEFAULT_CSV_FILE
        regions_to_process = read_lawd_codes_from_csv(csv_file)

    if not regions_to_process:
        print("❌ 처리할 지역 정보가 없습니다. --lawd 또는 --csv 옵션을 확인해 주세요.")
        return

    total_regions = len(regions_to_process)
    total_fetched_records = 0
    total_uploaded_records = 0
    total_db_duplicates_skipped = 0
    rls_blocked = False

    print(f"🚀 총 {total_regions}개 지역 × {len(ymd_list)}개 월 데이터 수집을 시작합니다...\n")

    # 2. 월별 / 지역별 수집 및 업로드 루프
    for ymd_idx, ymd in enumerate(ymd_list, 1):
        print(f"\n==================================================")
        print(f"🗓️ [{ymd_idx}/{len(ymd_list)}] {ymd[:4]}년 {ymd[4:]}월 데이터 작업 시작")
        print(f"==================================================")

        for reg_idx, reg in enumerate(regions_to_process, 1):
            lawd_cd = reg["lawd_cd"]
            full_name = reg["full_name"]

            print(f"[{reg_idx}/{total_regions}] {full_name}")

            # API 수집
            raw_items = fetch_rtms_data(lawd_cd, ymd, region_name=full_name)
            if not raw_items:
                continue

            total_fetched_records += len(raw_items)

            # 데이터 정제 및 메모리 1차 중복 제거
            cleaned_records = [clean_record(item) for item in raw_items]
            unique_records = deduplicate_records(cleaned_records)

            # DB 사전 대조: 이미 Supabase에 존재하는 레코드 조회
            existing_signatures = set()
            if not rls_blocked:
                existing_signatures = fetch_existing_db_signatures(
                    lawd_cd, ymd, SUPABASE_URL, args.key, TABLE_NAME
                )

            # DB에 존재하지 않는 순수 신규 데이터만 걸러내기
            new_records = []
            for r in unique_records:
                if get_record_signature(r) not in existing_signatures:
                    new_records.append(r)
                else:
                    total_db_duplicates_skipped += 1

            if existing_signatures:
                print(f"  └ 🔍 [DB 사전 검증] 기존 DB {len(existing_signatures)}건 존재 → 신규 {len(new_records)}건 대상 업로드")

            if not new_records:
                print("  └ ℹ️ 수집된 모든 데이터가 이미 DB에 존재하여 업로드를 건너뜁니다.")
                continue

            # Supabase 업로드
            if not rls_blocked:
                res = upload_to_supabase(
                    new_records, 
                    SUPABASE_URL, 
                    args.key, 
                    TABLE_NAME, 
                    resolution=args.on_conflict
                )
                if res == -1:
                    rls_blocked = True
                else:
                    total_uploaded_records += res

    print("\n" + "=" * 70)
    print("🎉 [전체 기간 처리 결과 요약]")
    print(f"  - 수집 기간:           {ymd_list[0]} ~ {ymd_list[-1]} ({len(ymd_list)}개월)")
    print(f"  - 처리한 지역 수:       {total_regions}개 지역")
    print(f"  - 총 API 수집 건수:     {total_fetched_records:,}건")
    print(f"  - DB 중복 제외 건수:    {total_db_duplicates_skipped:,}건")
    print(f"  - Supabase 신규 저장:   {total_uploaded_records:,}건")
    print("=" * 70)


if __name__ == "__main__":
    main()
