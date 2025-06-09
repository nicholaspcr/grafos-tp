package hub

import (
	depa "introduction.com/depA"
	depb "introduction.com/depB"
)

var text string = ""

func Text() string { return text }

func init() {
	text = depa.Text() + depb.Text()
}
