package main

import (
    "bytes"
    "fmt"
    "github.com/gorilla/websocket"
    "time"
)

const (
    maxMsgSize int64 = 256
    pongWait = 60 * time.Second
    pingPeriod = 10 * time.Second
)

type Client struct {
    send chan []byte
    hub *Hub
    conn *websocket.Conn
}

func (c *Client) Read() {
    defer func() {
        c.hub.logout <- c
        c.conn.Close()
    }()
    c.conn.SetReadLimit(maxMsgSize)
    c.conn.SetReadDeadline(time.Now().Add(pongWait))
    c.conn.SetPongHandler(func(appData string) error {
        c.conn.SetReadDeadline(time.Now().Add(pongWait))
        return nil
    })
    for {
        _, data, err := c.conn.ReadMessage()
        if err != nil {
            fmt.Printf("read from websocket error: %v", err)
            return
        }
        msg := bytes.TrimSpace(data)
        c.hub.broadcast <- msg
    }
}

func (c *Client) Write() {
    ticker := time.NewTicker(pingPeriod)
    defer func() {
        ticker.Stop()
        c.hub.logout <- c
        c.conn.Close()
    }()
    for {
        select {
        case msg, ok := <- c.send:
            if ok {
                c.conn.WriteMessage(websocket.TextMessage, msg)
                sLen := len(c.send)
                for i := 0; i < sLen; i++ {
                    c.conn.WriteMessage(websocket.TextMessage, <- c.send)
                }
            } else {
                c.conn.WriteMessage(websocket.CloseMessage, nil)
                return
            }
        case <- ticker.C:
            c.conn.SetWriteDeadline(time.Now().Add(20 * time.Second))
            if err := c.conn.WriteMessage(websocket.PingMessage, nil); err != nil {
                fmt.Printf("ping err: %v", err)
                return
            }
        }

    }
}