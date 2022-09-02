package main

import (
    "fmt"
    "io"
    "log"
)

// 自定义一个Reader，过滤掉非字母字符

func alpha(s byte) byte {
    if (s >= 'a' && s <= 'z') || (s >= 'A' && s <= 'Z') {
        return s
    } else {
        return 0
    }
}

type CustomReader struct {
    src string
    cur int //当前读取到的位置
}

func (cr *CustomReader) Read(buf []byte) (int, error) {
    if cr.cur >= len(cr.src) {
        return 0, io.EOF
    }
    //剩余待读取的字节长度
    remain := len(cr.src) - cr.cur

    var bundle int
    if remain >= len(buf) {
        bundle = len(buf)
    } else {
        bundle = remain
    }

    tempSl := make([]byte, bundle)
    for i := 0; i < bundle; i++ {
        if s := cr.src[cr.cur]; alpha(s) != 0 {
            tempSl[i] = s
        }
        cr.cur++
    }
    copy(buf, tempSl)
    return bundle, nil
}



func main() {
    myReader := CustomReader{src: "加walking with the light油"}
    sl := make([]byte, 3)

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
