package main

import (
	"github.com/gdamore/tcell/v2"
	"github.com/lk2322/p2p_messenger/network"
	"github.com/rivo/tview"
	"log"
	"net"
	"os"
	"time"
)

var app = tview.NewApplication()
var contacts []Contact
var currContact Contact
var messages = make(map[Contact][]Message)
var list = tview.NewList()
var textView = tview.NewTextView()
var inputField = tview.NewTextArea()

func initUI() {
	inputField.SetInputCapture(func(event *tcell.EventKey) *tcell.EventKey {
		if event.Key() == tcell.KeyEnter {
			ip, port := currContact.IP, currContact.Port
			text := inputField.GetText()
			network.Send(ip, port, text)
			inputField.SetText("", false)
			messages[currContact] = append(messages[currContact], Message{"You", text, time.Now()})
			updateTextView(currContact)

			return nil
		}
		if event.Key() == tcell.KeyTab {
			app.SetFocus(list)
			return nil
		}
		return event
	})
	inputField.SetBorder(true)
	inputField.SetTitle("Input")
	inputField.SetPlaceholder("Enter text here...")

	addContact := tview.NewForm().
		AddInputField("Name", "", 20, nil, nil).
		AddInputField("IP:PORT", "", 20, nil, nil)
	addContact.SetBorder(true)

	list.SetBorder(true).SetTitle("Contacts")

	textView.SetBorder(true).SetTitle("Chat")
	textView.SetDynamicColors(true)

	flex := tview.NewFlex().
		AddItem(list, 0, 1, true).
		AddItem(tview.NewFlex().SetDirection(tview.FlexRow).
			AddItem(textView, 0, 3, false).
			AddItem(inputField, 5, 1, false), 0, 3, false)

	pages := tview.NewPages().
		AddPage("main", flex, true, true).
		AddPage("form", CenterPrimitive(addContact, 40, 10), true, false)

	list.AddItem("[yellow]Add new contact", "", 0, func() {
		pages.ShowPage("form")
	}).
		AddItem("[red]Quit", "", 0, func() {
			app.Stop()
		}).ShowSecondaryText(false)

	addContact.AddButton("Save", func() {
		name := addContact.GetFormItem(0).(*tview.InputField)
		addr := addContact.GetFormItem(1).(*tview.InputField)
		ip, port, err := net.SplitHostPort(addr.GetText())
		if err != nil {
			pages.HidePage("form")
		}
		cont := Contact{name.GetText(), ip, port}
		contacts = append(contacts, cont)
		addContactToList(cont)
		clearInputFields(name, addr)
		//messages[cont] = append(messages[cont], Message{"You", "Hello world", time.Now()})
		//messages[cont] = append(messages[cont], Message{"FPfppfpf", "asdfsdf", time.Now()})

		pages.HidePage("form")

	}).AddButton("Quit", func() {
		clearInputFields(addContact.GetFormItem(0).(*tview.InputField),
			addContact.GetFormItem(1).(*tview.InputField))
		pages.HidePage("form")
	})
	if err := app.SetRoot(pages, true).SetFocus(flex).Run(); err != nil {
		panic(err)
	}
}

func getMessages() {
	server, err := network.CreateServer()
	if err != nil {
		log.Fatalln()
	}
	server.StartServer("8080")
	for msg := range server.MsgChan {
		ip, _, err := net.SplitHostPort(msg.Addr)
		if err != nil {
			log.Println(err)
			continue
		}
		text := msg.Text
		cont, flag := findContactByIP(ip, &contacts)
		if flag {
			m := Message{cont.Name, text, time.Now()}
			messages[cont] = append(messages[cont], m)
			updateTextView(cont)
			app.Draw()
		} else {
			cont = Contact{ip, ip, "8080"}
			contacts = append(contacts, cont)
			addContactToList(cont)
			app.Draw()
			m := Message{cont.Name, text, time.Now()}
			messages[cont] = append(messages[cont], m)

		}

	}

}

func main() {
	logFile, err := os.Create("logs.txt")
	if err != nil {
		return
	}
	log.SetOutput(logFile)
	go getMessages()
	initUI()

}
