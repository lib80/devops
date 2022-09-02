package main

import (
    "awesomeProject/dingding"
    "fmt"
    "github.com/hpcloud/tail"
    "strings"
)

func main() {
    t, _ := tail.TailFile("main/poem.txt", tail.Config{Follow: true})

    for line := range t.Lines {
       if strings.Contains(line.Text, "Exception") {
           fmt.Println("钉钉报警")
           dingding.SendNotify("golang测试")
       }
    }
}
