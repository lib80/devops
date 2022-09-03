package main

import (
    "crypto/tls"
    "fmt"
    "github.com/jlaffaye/ftp"
    "io"
    "os"
    "path"
    "time"
)

func CheckErr(err error) {
    if err != nil {
        panic(err)
    }
}

func main() {
    var (
       addr = "xxx:xxx"
       user = "xxx"
       password = "xxx"
       rootDir = "/somedir"
       downDir = "/data/ftp-files"
    )

    myTlsConfig := &tls.Config{
        InsecureSkipVerify: true,
        ClientAuth: tls.RequestClientCert,
    }

   c, err := ftp.Dial(addr, ftp.DialWithExplicitTLS(myTlsConfig), ftp.DialWithTimeout(5*time.Second))
   CheckErr(err)

   err = c.Login(user, password)
   CheckErr(err)

   err = os.MkdirAll(downDir, 0755)
   CheckErr(err)
   err = os.Chdir(downDir)
   CheckErr(err)

   walker := c.Walk(rootDir)
   for walker.Next() {
       f, err := os.Create(path.Base(walker.Path()))
       CheckErr(err)
       //defer f.Close()
       r, err := c.Retr(walker.Path())
       CheckErr(err)
       //defer r.Close()
       _, err = io.Copy(f, r)
       CheckErr(err)
       r.Close()
       f.Close()
   }
   fmt.Println("Successfully got all files!")
  
   //entries, err := c.List("/somepath")
   //for _, item := range entries {
   //    fmt.Println(item.Name)
   //}

}
