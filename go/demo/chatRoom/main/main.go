package main

import (
    "fmt"
    "github.com/gorilla/websocket"
    "net/http"
    "time"
)

func homeHandler(writer http.ResponseWriter, request *http.Request) {
    _, err := writer.Write([]byte("欢迎访问未来聊天室"))
    if err != nil {
        fmt.Println(err)
    }
}

func wsServer(upgrader *websocket.Upgrader, hub *Hub, writer http.ResponseWriter, request *http.Request) {
    conn, err := upgrader.Upgrade(writer, request, nil)
    if err != nil {
        fmt.Printf("fail to upgrade http to websocket: %v", err)
        return
    }
    defer conn.Close()
    client := &Client{
        send: make(chan []byte, 256),
        hub:  hub,
        conn: conn,
    }
    go client.Read()
    go client.Write()
}

func main() {
    upgrader := &websocket.Upgrader{
        HandshakeTimeout: 3 * time.Second,
        ReadBufferSize: 512,
        WriteBufferSize: 512,
        CheckOrigin: func(r *http.Request) bool {
            return true
        },
    }
    hub := NewHub()
    http.HandleFunc("/", homeHandler)
    http.HandleFunc("/ws", func(writer http.ResponseWriter, request *http.Request) {
        wsServer(upgrader, hub, writer, request)
    })
    go hub.Run()
    http.ListenAndServe("localhost:8080", nil)
}
