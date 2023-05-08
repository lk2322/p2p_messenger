package main

import "time"

type Contact struct {
	Name string
	IP   string
	Port string
}
type Message struct {
	From string
	Text string
	time time.Time
}
