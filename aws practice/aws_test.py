import boto3
import uuid
import pprint
import json
from terminaltables import DoubleTable

session = boto3.session.Session()

s3_client = boto3.client('s3')

s3_resource = boto3.resource('s3')

client = boto3.client('support')

def create_bucket_name(bucket_prefix):
    return ''.join([bucket_prefix, str(uuid.uuid4())])

def create_bucket(bucket_prefix, s3_connection):

    current_region = session.region_name
    bucket_name = create_bucket_name(bucket_prefix)
    bucket_response = s3_connection.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
        'LocationConstraint': current_region})
    print(bucket_name, current_region)
    return bucket_name, bucket_response

#first_bucket_name, first_response = create_bucket(
  #  bucket_prefix='firstpybucket',
   # s3_connection=s3_resource)

# second_bucket_name, second_response = create_bucket(
#     bucket_prefix='secondpybucket',
#     s3_connection=s3_resource)
# print(first_response)
# print(second_response)

def create_temp_file(size, file_name, file_contet):
    random_file_name = ''.join([str(uuid.uuid4().hex[:6]), file_name])
    with open(random_file_name, 'w') as f:
        f.write(str(file_contet) * size)
    return random_file_name

#first_file_name = create_temp_file(300, 'firstFile.txt', 'f')

# upload
def upload_file(bucket_name, file_name, upload_type, encryption):
    if upload_type == 'public' & encryption == 'yes':
        s3_resource.Object(bucket_name, file_name).upload_file(Filename=file_name, ExtraArgs={
            'ACL': 'public-read',
            'ServerSideEncryption': 'AES256'})
    elif upload_type == 'public' & encryption == 'no':
                s3_resource.Object(bucket_name, file_name).upload_file(Filename=file_name, ExtraArgs={
            'ServerSideEncryption': 'AES256'})
    else:
        s3_resource.Object(bucket_name, file_name).upload_file(Filename=file_name)
    

def copy_to_bucket(from_bucket, to_bucket, file_name):
    copy_source = {
        'Bucket': from_bucket,
        'Key': file_name
    }
    s3_resource.Object(to_bucket, file_name).copy(copy_source)

def delete_file(from_bucket, file_name):
    s3_resource.Object(from_bucket, file_name)

def enable_bucket_versioning(bucket_name):
    bkt_versioning = s3_resource.BucketVersioning(bucket_name)
    bkt_versioning.enable()

def delete_all_objects(bucket_name):
    objs = []
    bucket = s3_resource.Bucket(bucket_name)
    for obj_version in bucket.object_versions.all():
        objs.append({'Key': obj_version.object_key,
        'VersionId': obj_version.id})
    bucket.delete_objects(Delete={'Objects': objs})

def bucket_metrics(cw_cli, bucket_name):
    measurable_metrics = [
        ('BucketSizeBytes', 'StandardStorage'),
        ('NumberOfObjects', 'AllStorageTypes'),
    ]

    date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    results = {}

    for metric_name, storage_type in measurable_metrics:
        metrics = cw_cli.get_metric_statistics(
            Namespace='AWS/S3',
            MetricName=metric_name,
            Dimensions=[
                {'Name': 'BucketName', 'Value': bucket_name},
                {'Name': 'StorageType', 'Value': storage_type}
            ],
            Statistics=['Average'],
            Period=86400,
            StartTime=date - timedelta(days=7),
            EndTime=date
        )

        if metrics.get('Datapoints'):
            results[metric_name] = sorted(
                metrics.get('Datapoints'), 
                key=lambda row: row.get('Timestamp')
                )[-1].get('Average')

    return {
        'bucket_name': bucket_name,
        'bucket_items': results.get('NumberOfObjects'),
        'bucket_size': results.get('BucketSizeBytes')
    }


file_count = 0
total_space = 0
pp = pprint.PrettyPrinter(width=100, compact=True)
public_buckets = []
private_buckets = []


for bucket in s3_resource.buckets.all():
    buckett = bucket.name

    results = s3_client.get_bucket_acl(Bucket=buckett)
    #result = s3_client.get_bucket_policy_status(Bucket=buckett)

    for result in results['Grants']:
        if 'URI' in result['Grantee'] and 'AllUser' in result['Grantee']['URI']:
            public_buckets.append(buckett)

    if buckett not in public_buckets:
        private_buckets.append(buckett)

# for item in public_buckets:
#     s.add(item)
print(set(public_buckets))

print(private_buckets)

# for b in s:
#     bucket_name = b

#     for obj in s3_resource.Bucket(bucket_name).objects.all():
#         file_count = file_count + 1
#         print(obj.key + ' ' + str(obj.size) + 'B')
#         total_space = total_space + obj.size
#         print('Total space taken in this bucket: ' + str(total_space) + 'B')
# print('--------------------------------------------------------')

#with the other account
# checks = client.describe_trusted_advisor_checks(language='en').get('checks')
# pp = pprint.PrettyPrinter(width=100, compact=True)
# pp.pprint(checks)

# check_ids = [
#     check.get('id')
#     for check in checks
#     if check.get('name') in ['Amazon S3 Bucket Permissions']
# ]
# print(check_ids)

# check_ids = []
# for check in checks:
#     if check.get('name') in ['Low Utilization Amazon EC2 Instances']:
#         check_ids.append(check.get('id'))


# print(checks)



# result = s3_client.get_bucket_policy_status(Bucket='secondpybucket146abccd-5dc1-4b4e-a63c-a0747f1782e6')
# print(result['PolicyStatus'])
#download
#s3_resource.Object(first_bucket_name, first_file_name).download_file(f'/tmp/{first_file_name}')