// 火箭发射倒计时
package main

import (
    "fmt"
    "os"
    "time"
)

func CountDown(n int, countCh chan int, finishCh chan struct{}) {
    if n <= 0 {
        return
    }
    tk := time.NewTicker(1 * time.Second)
    for {
        countCh <- n
        <- tk.C
        n--
        if n <= 0 {
            tk.Stop()
            finishCh <- struct{}{}
            break
        }
    }
}

func Abort(abortCh chan struct{}) {
    b := make([]byte, 1)
    os.Stdin.Read(b)  //阻塞直到从标准输入获取到数据
    abortCh <- struct{}{}
}

func main() {
    var (
        countCh = make(chan int)
        finishCh = make(chan struct{})
        abortCh = make(chan struct{})
    )
    go CountDown(10, countCh, finishCh)
    go Abort(abortCh)
    Loop:
    for {
        select {
        case n := <- countCh:
            fmt.Println(n)
        case <- finishCh:
            fmt.Println("发射!")
            break Loop
        case <- abortCh:
            fmt.Println("中止")
            break Loop
        }
    }
}
