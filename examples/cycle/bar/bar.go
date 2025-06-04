package bar

import "cycle.com/definition"

type b struct{}

func (*b) Message() string { return "Bar" }

func New() definition.FooBar { return &b{} }
