import requests
import json
import time
import stadata

API_KEY = "7d61b14ed6901581dda8958dac559433"
BASE_API = f"https://webapi.bps.go.id/v1/api/view/domain/3471/model/statictable/lang/ind/key/{API_KEY}/id/"

# list tabel
client = stadata.Client(API_KEY)
tables = client.list_statictable(domain=['3471'])
result = tables.to_dict(orient='records')
print(f"Total {len(result)} tabel ditemukan.")

# detail tiap tabel
all_detail = []
for i, row in enumerate(result):
    table_id = row['table_id']
    print(f"[{i+1}/{len(result)}] ID {table_id}: {row['title'][:50]}...")
    
    try:
        r = requests.get(BASE_API + str(table_id), timeout=15)
        data = r.json()
        
        if data.get('status') == 'OK':
            tabel_data = data['data']
            all_detail.append({
                "table_id": str(table_id),
                "title": row['title'],
                "subj": row['subj'],
                "updt_date": str(row['updt_date']),
                "size": row['size'],
                "table": tabel_data.get('table', ''),
                "excel": tabel_data.get('excel', ''),
            })
            print(f"  ✅ OK")
        else:
            all_detail.append({
                "table_id": str(table_id),
                "title": row['title'],
                "subj": row['subj'],
                "updt_date": str(row['updt_date']),
                "size": row['size'],
                "table": "",
                "excel": "",
            })
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    time.sleep(0.3)

with open("tabel_statistik.json", "w", encoding="utf-8") as f:
    json.dump(all_detail, f, ensure_ascii=False, indent=2)

print(f"\n {len(all_detail)} tabel disimpan.")
