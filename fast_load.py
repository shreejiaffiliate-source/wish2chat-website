import json
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wish2chat.settings')
django.setup()

from core.models import Content

def run_bulk_upload():
    with open('part3_content.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    objects = []
    total = len(data)
    print(f"Total records found: {total}")

    for i, item in enumerate(data):
        fields = item['fields']
        
        # JADU: Yahan hum Foreign Key IDs ko rename kar rahe hain
        # Agar error 'sub_category' par hai, toh use 'sub_category_id' bana do
        if 'sub_category' in fields:
            fields['sub_category_id'] = fields.pop('sub_category')
        
        # Agar user ya kisi aur field mein bhi same error aaye toh ye line add kar dena:
        # if 'user' in fields: fields['user_id'] = fields.pop('user')

        obj = Content(id=item['pk'], **fields)
        objects.append(obj)

        if len(objects) == 500:
            Content.objects.bulk_create(objects, ignore_conflicts=True)
            objects = []
            print(f"Uploaded {i+1}/{total}...")

    if objects:
        Content.objects.bulk_create(objects, ignore_conflicts=True)
    
    print("Mubarak ho! 18,349 records load ho gaye.")

if __name__ == "__main__":
    run_bulk_upload()