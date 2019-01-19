from azure.storage.blob import BlockBlobService

def upload_blob(filename, filepath):
    block_blob_service = BlockBlobService(
        account_name='facturefracture',
        account_key='53komISgN0kGVHUKNj9e55u9h9avf09dyu/unBadeROztPv9rak/UvWwmCejmgm9DnWXJtLUU9THU08pIihzIw==')

    block_blob_service.create_blob_from_path('bills-images', filename, filepath)
