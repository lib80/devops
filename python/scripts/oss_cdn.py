#!/usr/bin/env python3
# coding=utf-8
# Author: libin

import time
import oss2
from oss2.models import LifecycleExpiration, LifecycleRule, BucketLifecycle, AbortMultipartUpload
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcdn.request.v20180510.AddCdnDomainRequest import AddCdnDomainRequest


access_key_id = ''
access_key_secret = ''
region = ''
oss_endpoint = ''
prefix = ''  # 项目名前缀
domain_name = 'xxx.com'
bucket_suffix_list = {
    'bucket01': 1,
    'bucket02': 1,
    'bucket03': 0
}  # 0代表私有，1代表公共读


def create_bucket():
    auth = oss2.Auth(access_key_id, access_key_secret)
    for name, pri_code in bucket_suffix_list.items():
        bucket_name = prefix + name
        bucket = oss2.Bucket(auth, oss_endpoint, bucket_name, connect_timeout=30)
        if pri_code:
            bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        else:
            bucket.create_bucket(oss2.models.BUCKET_ACL_PRIVATE)
        if name is 'chatfile':
            # 给chatfile设置生命周期规则
            rule1 = LifecycleRule('rule1', '', status=LifecycleRule.ENABLED, expiration=LifecycleExpiration(days=7),
                                  abort_multipart_upload=AbortMultipartUpload(days=7))
            lifecycle = BucketLifecycle([rule1])
            bucket.put_bucket_lifecycle(lifecycle)

    time.sleep(3)
    service = oss2.Service(auth, oss_endpoint)
    bucket_list = [b.name for b in oss2.BucketIterator(service)]
    return bucket_list


def create_cdn(bucket_list):
    client = AcsClient(access_key_id, access_key_secret, region)

    request = AddCdnDomainRequest()
    request.set_accept_format('json')

    request.set_CdnType("web")
    request.set_Scope("overseas")
    for bucket in bucket_list:
        full_domain_name = bucket + '.' + domain_name
        bucket_api = bucket + '.' + oss_endpoint
        request.set_DomainName(full_domain_name)
        request.set_Sources("[{'type':'oss','content':'%s'}]" % bucket_api)
        response = client.do_action_with_exception(request)
        print(str(response, encoding='utf-8'))


if __name__ == '__main__':
    bucket_list = create_bucket()
    create_cdn(bucket_list)
