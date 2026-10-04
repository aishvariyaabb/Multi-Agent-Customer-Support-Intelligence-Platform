import requests, json

payload = {
 'customer_name':'Aish',
 'customer_email':'aish@gmail.com',
 'subject':'Shoe rack',
 'description':'The shoe rack received in order #ORD8038374 has scratches and dents. Looks like a returned/used item.',
 'use_knowledge_base': True,
 'enable_escalation': True
}

try:
    r = requests.post('http://127.0.0.1:8000/api/v1/process', json=payload, timeout=60)
    data = r.json()
    with open('last_response.json','w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('SAVED last_response.json', 'STATUS', r.status_code)
except Exception as e:
    print('ERROR', e)
