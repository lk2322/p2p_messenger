package network

import (
	p2p "github.com/lk2322/golang-p2p"
	"log"
)

func Send(hostname string, port string, msg string) {
	tcp := p2p.NewTCP(hostname, port)
	client, err := p2p.NewClient(tcp)
	client.SetLogger(Logger{})
	if err != nil {
		log.Fatalln(err)
	}
	req := p2p.Data{}
	err = req.SetGob(p2pMsg{msg})
	if err != nil {
		log.Println(err)
		return
	}
	_, err = client.Send("dialog", req)
	if err != nil {
		log.Println(err)
		return
	}
}
