package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"sync"

	petstore "github.com/dev-shimada/ogen-playground/api/petstore"
	httpSwagger "github.com/swaggo/http-swagger/v2"
)

type petsService struct {
	pets map[int64]petstore.Pet
	mux  sync.Mutex
}

func (p *petsService) AddPet(ctx context.Context, req *petstore.Pet) (*petstore.Pet, error) {
	p.mux.Lock()
	defer p.mux.Unlock()

	// リクエストで指定されたIDを使用
	if id, ok := req.ID.Get(); ok {
		p.pets[id] = *req
	}
	return req, nil
}

func (p *petsService) DeletePet(ctx context.Context, params petstore.DeletePetParams) error {
	p.mux.Lock()
	defer p.mux.Unlock()

	delete(p.pets, params.PetId)
	return nil
}

func (p *petsService) GetPetById(ctx context.Context, params petstore.GetPetByIdParams) (petstore.GetPetByIdRes, error) {
	p.mux.Lock()
	defer p.mux.Unlock()

	pet, ok := p.pets[params.PetId]
	if !ok {
		// Return Not Found.
		return &petstore.GetPetByIdNotFound{}, nil
	}
	return &pet, nil
}

func (p *petsService) UpdatePet(ctx context.Context, params petstore.UpdatePetParams) error {
	p.mux.Lock()
	defer p.mux.Unlock()

	pet := p.pets[params.PetId]
	pet.Status = params.Status
	if val, ok := params.Name.Get(); ok {
		pet.Name = val
	}
	p.pets[params.PetId] = pet

	return nil
}

func main() {
	// Create service instance.
	service := &petsService{
		pets: map[int64]petstore.Pet{},
	}
	// Create generated server.
	srv, err := petstore.NewServer(service)
	if err != nil {
		log.Fatal(err)
	}
	mux := http.NewServeMux()
	mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("OK"))
	})

	// Serve OpenAPI specification file
	mux.HandleFunc("/openapi.yaml", func(w http.ResponseWriter, r *http.Request) {
		data, err := os.ReadFile("petstore.yaml")
		if err != nil {
			http.Error(w, "Failed to read OpenAPI spec", http.StatusInternalServerError)
			return
		}
		w.Header().Set("Content-Type", "application/x-yaml")
		w.Write(data)
	})

	// Serve Swagger UI
	mux.Handle("/docs/", httpSwagger.Handler(
		httpSwagger.URL("/openapi.yaml"),
	))

	mux.Handle("/v3/", http.StripPrefix("/v3", srv))

	log.Println("Server started at :8080")
	if err := http.ListenAndServe(":8080", mux); err != nil {
		log.Fatal(err)
	}
}
