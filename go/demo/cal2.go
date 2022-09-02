package server

import "sync"

const workersNum = 10

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
    for i := 0; i < workersNum; i++ {
        wg.Add(1)
        go processTask(taskChan, wg)
    }
    wg.Wait()
    close(resChan)
}

func processTask(taskChan <-chan task, wg *sync.WaitGroup) {
    //多个goroutine并行读取task chan
    defer wg.Done()
    for t := range taskChan {
        t.cal()
    }    
}

func processRes(resChan chan int) int {
    sum := 0
    for r := range resChan {
        sum += r
    }
    return sum
}

func Cal(num int) int {
    //可用于计算1000以内自然数的和
    //并发模式：固定worker工作池
    taskChan := make(chan task, 100)
    resChan := make(chan int, 100)

    wg := &sync.WaitGroup{}
    initTask(taskChan, resChan, num)
    distributeTask(taskChan, wg, resChan)
    sum :=  processRes(resChan)
    return sum
}
