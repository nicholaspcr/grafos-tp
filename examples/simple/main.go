package main

import (
	"fmt"

	"example.com/bar"
	"example.com/foo"
)

func main() {
	foo.Foo()
	bar.Bar()
	fmt.Println("Simple test without cycles")
}
