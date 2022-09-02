package main

import (
    "fmt"
    "log"
    "sync"
    "time"
)

/*
这是用interface和map实现的一个发布系统
能发布k8s、node等不同类型的任务
支持增量更新：启动新的，停止旧的
*/

type deployJob interface {
    start()
    stop()
    hash() string
}

type K8sD struct {
    id   int
    name string
}

func (kd *K8sD) start() {
    log.Printf("k8s deploy start: id: %d, name: %s", kd.id, kd.name)
}

func (kd *K8sD) stop() {
    log.Printf("k8s deploy stop: id: %d, name: %s", kd.id, kd.name)
}

func (kd *K8sD) hash() string {
    return kd.name
}

type hostD struct {
    id   int
    name string
}

func (hd *hostD) start() {
    log.Printf("host deploy start: id: %d, name: %s", hd.id, hd.name)
}

func (hd *hostD) stop() {
    log.Printf("host deploy stop: id: %d, name: %s", hd.id, hd.name)
}

func (hd *hostD) hash() string {
    return hd.name
}

type jobManager struct {
    sync.RWMutex
    activeTarges map[string]deployJob
}

func (jm *jobManager) sync(jobs []deployJob) {

    allJobMap := make(map[string]deployJob)
    jm.Lock()
    defer jm.Unlock()
    //添加并启动新的: jobs中有而activeTarges没有的，添加并启动
    for _, job := range jobs {
        mark := job.hash()
        allJobMap[mark] = job
        if _, exist := jm.activeTarges[mark]; !exist {
            jm.activeTarges[mark] = job
            job.start()
        }
    }

    //停止并删除旧的：activeTarges中有而jobs中没有的，停止并删除
    for mark, job := range jm.activeTarges {
        if _, ok := allJobMap[mark]; !ok {
            job.stop()
            delete(jm.activeTarges, mark)
        }
    }
}

func main() {
    jm := &jobManager{activeTarges: make(map[string]deployJob)}
    jobs1 := make([]deployJob, 0)
    jobs2 := make([]deployJob, 0)
    for i := 0; i < 3; i++ {
        jobs1 = append(jobs1, &K8sD{id: i, name: fmt.Sprintf("k8s_deploy_job_%d", i)}, &hostD{id: i, name: fmt.Sprintf("host_deploy_job_%d", i)})
    }
    for i := 2; i < 5; i++ {
        jobs2 = append(jobs2, &K8sD{id: i, name: fmt.Sprintf("k8s_deploy_job_%d", i)}, &hostD{id: i, name: fmt.Sprintf("host_deploy_job_%d", i)})
    }
    go jm.sync(jobs1)
    go jm.sync(jobs2)
    time.Sleep(time.Second * 30)
}
