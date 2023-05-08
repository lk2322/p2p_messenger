package main

import (
	"fmt"
	"github.com/rivo/tview"
)

func clearInputFields(fields ...*tview.InputField) {
	for _, field := range fields {
		field.SetText("")
	}

}

func updateTextView(contact Contact) {

	app.SetFocus(inputField)
	textView.Clear()
	wr := textView.BatchWriter()
	defer func(wr tview.TextViewWriter) {
		err := wr.Close()
		if err != nil {

		}
	}(wr)
	for _, msg := range messages[contact] {
		switch name := msg.From; name {
		case "You":
			_, err := fmt.Fprintf(wr, "[red]>%s: [white]%s\n", msg.From, msg.Text)
			if err != nil {
				return
			}
		default:
			_, err := fmt.Fprintf(wr, "[blue]>%s: [white]%s\n", msg.From, msg.Text)
			if err != nil {
				return
			}

		}

	}
}

func addContactToList(contact Contact) {
	list.AddItem(contact.Name, "", 0, func() {
		currContact = contact
		updateTextView(contact)
	})
}

func findContactByIP(ip string, contacts *[]Contact) (Contact, bool) {
	for _, cont := range *contacts {
		if cont.IP == ip {
			return cont, true
		}
	}
	return Contact{}, false
}
