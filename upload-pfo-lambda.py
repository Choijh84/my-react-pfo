import boto3
from botocore.client import Config
import StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):
    s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
    
    pfo_bucket = s3.Bucket('serverless-react-pfo')
    build_bucket = s3.Bucket('serverless-pfo-build')
    
    pfo_zip = StringIO.StringIO()
    build_bucket.download_fileobj('portfoliobuild.zip',  pfo_zip)
    
    with zipfile.ZipFile(pfo_zip) as myzip: 
        for nm in myzip.namelist(): 
            obj = myzip.open(nm)
            pfo_bucket.upload_fileobj(obj, nm, 
                ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
            pfo_bucket.Object(nm).Acl().put(ACL='public-read')
            
    return 'Hello World'
            

