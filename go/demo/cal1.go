package main

import (
    "fmt"
    "sync"
)

type task struct {
    begin int
    end int
    result chan<- int
}

func initTask(taskChan chan<- task, resChan chan int, num int) {
    qu := num / 10
    mod := num % 10
    for i := 0; i < qu; i++ {
        taskChan <- task{
            begin: i * 10 + 1,
            end: (i + 1) * 10,
            result: resChan,
        }
    }
    if mod != 0 {
        taskChan <- task{
            begin: qu * 10,
            end: num,
            result: resChan,
        }
    }
    close(taskChan)
}

func (t *task) cal() {
    sum := 0
    for i := t.begin; i <= t.end; i++ {
        sum += i
    }
    t.result <- sum
}

func distributeTask(taskChan <-chan task, wg *sync.WaitGroup, resChan chan int) {
    for t := range taskChan {
        wg.Add(1)
        go processTask(t, wg)
    }
    wg.Wait()
    close(resChan)
}

func processTask(t task, wg *sync.WaitGroup) {
    defer wg.Done()
    t.cal()    
}

func processRes(resChan chan int) int {
    sum := 0
    for r := range resChan {
        sum += r
    }
    return sum
}

func main() {
    //可用于计算1000以内自然数之和
    //并发模式：分为多个task，一个task一个goroutine
    taskChan := make(chan task, 100)
    resChan := make(chan int, 100)
    wg := &sync.WaitGroup{}
    initTask(taskChan, resChan, 110)
    distributeTask(taskChan, wg, resChan)
    sum :=  processRes(resChan)
    fmt.Println(sum)
}
