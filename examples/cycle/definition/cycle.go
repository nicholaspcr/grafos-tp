package definition

import (
	"fmt"

	"cycle.com/bar"
	"cycle.com/foo"
)

func CreateCycle() {
	fmt.Println(foo.New(), bar.New())
}
