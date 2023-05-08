package network

import (
	"context"
	p2p "github.com/lk2322/golang-p2p"
	"log"
)

type Server struct {
	MsgChan chan Message
}

func CreateServer() (Server, error) {
	c := make(chan Message, 10)
	return Server{c}, nil

}

func (s Server) StartServer(port string) {
	go func() {
		defer close(s.MsgChan)
		tcp := p2p.NewTCP("0.0.0.0", port)
		server, err := p2p.NewServer(tcp)
		server.SetLogger(Logger{})
		if err != nil {
			log.Panicln(err)
		}
		server.SetHandler("dialog", s.handle)
		err = server.Serve()
		if err != nil {
			log.Fatalln(err)

		}
	}()
}
func (s Server) handle(_ context.Context, data p2p.Data) (err error) {
	msg := p2pMsg{}
	err = data.GetGob(&msg)
	if err != nil {
		log.Println(err)
		return
	}
	s.MsgChan <- Message{msg.Text, data.Addr}
	return
}
