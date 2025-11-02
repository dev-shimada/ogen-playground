package main

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"os"

	"github.com/fatih/color"

	petstore "github.com/dev-shimada/ogen-playground/client/petstore"
)

func run(ctx context.Context) error {
	var arg struct {
		BaseURL string
		ID      int64
	}
	flag.StringVar(&arg.BaseURL, "url", "http://api:8080/v3", "target server url")
	flag.Int64Var(&arg.ID, "id", 1, "pet id to request")
	flag.Parse()

	client, err := petstore.NewClient(arg.BaseURL)
	if err != nil {
		return fmt.Errorf("create client: %w", err)
	}

	// Create a new pet first
	newPet := &petstore.Pet{
		ID:     petstore.NewOptInt64(arg.ID),
		Name:   "Dog",
		Status: petstore.NewOptPetStatus(petstore.PetStatusAvailable),
	}

	createdPet, err := client.AddPet(ctx, newPet)
	if err != nil {
		return fmt.Errorf("create pet: %w", err)
	}

	color.New(color.FgYellow).Println("Pet created successfully:")
	data, err := createdPet.MarshalJSON()
	if err != nil {
		return err
	}
	var out bytes.Buffer
	if err := json.Indent(&out, data, "", "  "); err != nil {
		return err
	}
	color.New(color.FgYellow).Println(out.String())

	// Get the pet by ID
	res, err := client.GetPetById(ctx, petstore.GetPetByIdParams{
		PetId: arg.ID,
	})
	if err != nil {
		return fmt.Errorf("get pet %d: %w", arg.ID, err)
	}

	switch p := res.(type) {
	case *petstore.Pet:
		color.New(color.FgGreen).Println("\nPet retrieved successfully:")
		data, err := p.MarshalJSON()
		if err != nil {
			return err
		}
		var out bytes.Buffer
		if err := json.Indent(&out, data, "", "  "); err != nil {
			return err
		}
		color.New(color.FgGreen).Println(out.String())
	case *petstore.GetPetByIdNotFound:
		return errors.New("not found")
	}

	return nil
}

func main() {
	if err := run(context.Background()); err != nil {
		color.New(color.FgRed).Printf("%+v\n", err)
		os.Exit(2)
	}
}
