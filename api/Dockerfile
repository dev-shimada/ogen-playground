FROM --platform=$BUILDPLATFORM golang:1.25.3-trixie AS build

ARG TARGETPLATFORM
ARG BUILDPLATFORM
ARG TARGETOS
ARG TARGETARCH

WORKDIR /workspace

RUN  <<EOF
# grpc_health_probe
go install github.com/grpc-ecosystem/grpc-health-probe@latest
EOF

COPY go.mod /workspace
COPY go.sum /workspace
RUN go mod download
COPY petstore /workspace/petstore
COPY main.go /workspace
COPY petstore.yaml /workspace
RUN CGO_ENABLED=0 GOOS=${TARGETOS} GOARCH=${TARGETARCH} go build -o bin/app main.go


FROM --platform=$BUILDPLATFORM gcr.io/distroless/base-debian12:latest
WORKDIR /app
COPY --from=build /workspace/bin/app /app/app
COPY --from=build /workspace/petstore.yaml /app/petstore.yaml
COPY --from=build /go/bin/grpc-health-probe /bin/grpc-health-probe
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s CMD ["/bin/grpc-health-probe", "-addr=:8080/health"]
EXPOSE 8080
ENTRYPOINT [ "/app/app" ]
