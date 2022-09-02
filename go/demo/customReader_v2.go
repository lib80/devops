package main

import (
    "fmt"
    "io"
    "log"
    "os"
)

// 自定义一个Reader，并组合其它Reader, 过滤掉非字母字符

func alpha(s byte) byte {
    if (s >= 'a' && s <= 'z') || (s >= 'A' && s <= 'Z') {
        return s
    } else {
        return 0
    }
}

type CustomReader struct {
    reader io.Reader
}

func (cr *CustomReader) Read(buf []byte) (int, error) {
    n, err := cr.reader.Read(buf)
    if err == io.EOF {
        return n, err
    }
    tempSl := make([]byte, n)
    for i := 0; i < n; i++ {
        if s := buf[i]; alpha(s) != 0 {
            tempSl[i] = s
        }
    }
    copy(buf, tempSl)
    return n, err
}



func main() {
    file, err := os.Open("main/poem.txt")    
    if err != nil {
        fmt.Println(err)
        return
    }
    defer file.Close()
    myReader := CustomReader{reader: file}
    sl := make([]byte, 4)

    for {
     n, err := myReader.Read(sl)
     if err != nil {
         if err == io.EOF {
             break
         } else {
             fmt.Printf("未知错误：%v\n", err)
             return
         }
     }
     log.Printf("读取到：%s\n", string(sl[:n]))
    }
}
