package foo

import "cycle.com/definition"

type f struct{}

func (*f) Message() string { return "Foo" }

func New() definition.FooBar { return &f{} }
