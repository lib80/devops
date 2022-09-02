package main

type Hub struct {
    clients map[*Client]bool
    broadcast chan []byte
    login chan *Client
    logout chan *Client
}

func NewHub() *Hub {
    return &Hub{
        clients: make(map[*Client]bool),
        broadcast: make(chan []byte),
        login: make(chan *Client),
        logout: make(chan *Client),
    }
}

func (h *Hub) Run() {
    for {
        select {
        case msg := <- h.broadcast:
            for c := range h.clients {
                select {
                case c.send <- msg:
                default:
                    close(c.send)
                    delete(h.clients, c)
                }
            }
        case c := <- h.login: h.clients[c] = true
        case c := <- h.logout:
            close(c.send)
            delete(h.clients, c)
        }
    }
}