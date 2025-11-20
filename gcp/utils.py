from gcp.paths import BUCKET_NAME
from google.cloud import storage
import io


bucket = storage.Client().bucket(BUCKET_NAME)

def upload_to_gcp(dic):
    for path, df in dic.items():
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        blob = bucket.blob(path)
        blob.upload_from_string(csv_buffer.getvalue(), content_type='text/csv')
        print(f'Archivo subido a GCP: {path}')
