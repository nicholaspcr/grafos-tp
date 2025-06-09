package depb

var text string = ""

func Text() string { return text }

func init() {
	text = "bar"
}
