/*
该脚本用于过滤大小为0的对象
author: libin
*/
package main

import (
	"context"
	"fmt"
	"os"
	"strings"
	"sync"
	"time"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/credentials"
	"github.com/aws/aws-sdk-go-v2/service/s3"
	"github.com/aws/aws-sdk-go-v2/service/s3/types"
)

const (
	workersNum    = 20
	outFileSuffix = "size0_objects.txt"
)

type bucketObjects struct {
	bucketName string
	objects    []types.Object
}

var mu sync.Mutex

func writeFile(data string, bucketName string) {
	outFile := fmt.Sprintf("%v_%v", bucketName, outFileSuffix)
	mu.Lock()
	defer mu.Unlock()	
	file, err := os.OpenFile(outFile, os.O_APPEND|os.O_WRONLY|os.O_CREATE, 0644)
	if err != nil {
		fmt.Println("文件打开错误", err)
		return
	}
	defer file.Close()
	_, err = file.WriteString(data)
	if err != nil {
		fmt.Println("数据写入失败", err)
		return
	}
}

func filter0SizeObjects(taskChan <-chan bucketObjects, wg *sync.WaitGroup) {
	defer wg.Done()
	var b strings.Builder
	for bucketObjects := range taskChan {
		for _, obj := range bucketObjects.objects {
			if obj.Size == 0 {
				b.WriteString(aws.ToString(obj.Key) + "\n")
			}
		}
		if b.Len() != 0 {
			writeFile(b.String(), bucketObjects.bucketName)
			b.Reset()
		}
	}
}

func distributeTask(taskChan <-chan bucketObjects, wg *sync.WaitGroup) {
	for i := 0; i < workersNum; i++ {
		wg.Add(1)
		go filter0SizeObjects(taskChan, wg)
	}
}

func generateTask(client *s3.Client, bucketName string, taskChan chan<- bucketObjects, wg *sync.WaitGroup) {
	defer wg.Done()
	marker := ""
	maxKeys := 1000
	truncated := true
	for truncated {
		output, err := client.ListObjects(context.TODO(), &s3.ListObjectsInput{
			Bucket:  aws.String(bucketName),
			Marker:  aws.String(marker),
			MaxKeys: int32(maxKeys),
		})

		if err != nil {
			fmt.Println(err)
			break
		}
		truncated = output.IsTruncated
		objs := output.Contents
		if len(objs) > 0 {
			marker = aws.ToString(objs[len(objs)-1].Key)
			taskChan <- bucketObjects{bucketName: bucketName, objects: objs}
		}
	}
}

func main() {
	fmt.Println("begin:", time.Now().Format("2006-01-02 15:04:05"))

	endpoint := "http://xxx:xxx"
	accessKey := "xxx"
	secretKey := "xxx"

	config := aws.Config{
		Credentials: credentials.NewStaticCredentialsProvider(accessKey, secretKey, ""),
		EndpointResolverWithOptions: aws.EndpointResolverWithOptionsFunc(func(service, region string, options ...interface{}) (aws.Endpoint, error) {
			return aws.Endpoint{URL: endpoint}, nil
		}),
	}

	client := s3.NewFromConfig(config, func(o *s3.Options) {
		o.UsePathStyle = true
		o.EndpointOptions.DisableHTTPS = true
	})

	taskChan := make(chan bucketObjects, 100)
	wgGenTask := &sync.WaitGroup{}
	wgProcessTask := &sync.WaitGroup{}
	go distributeTask(taskChan, wgProcessTask)

	output, err := client.ListBuckets(context.TODO(), &s3.ListBucketsInput{})
	if err != nil {
		fmt.Println(err)
		os.Exit(-1)
	}
	buckets := output.Buckets
	for _, bucket := range buckets {
		//fmt.Println(aws.ToString(bucket.Name))
		wgGenTask.Add(1)
		go generateTask(client, aws.ToString(bucket.Name), taskChan, wgGenTask)
	}

	wgGenTask.Wait()
	close(taskChan)
	wgProcessTask.Wait()
	fmt.Println("end:", time.Now().Format("2006-01-02 15:04:05"))
}

