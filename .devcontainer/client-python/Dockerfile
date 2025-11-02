FROM --platform=$BUILDPLATFORM python:3.14-trixie AS vscode

ARG TARGETPLATFORM
ARG BUILDPLATFORM
ARG TARGETOS
ARG TARGETARCH
ENV PATH=$PATH:/root/.local/bin

WORKDIR /workspace/client-python

RUN  <<EOF
apt-get update && apt-get install -y vim git unzip less bash-completion jq npm pipx
pipx install uv openapi-python-client
npm i -g @anthropic-ai/claude-code
# bash completions
echo "source /usr/share/bash-completion/completions/git" >> ~/.bashrc
echo "source <(buf completion bash)" >> ~/.bashrc
EOF

# COPY pyproject.toml /workspace/client-python/

# RUN <<EOF
# pip install uv
# uv pip install --system -r pyproject.toml
# EOF

# COPY . /workspace/client-python/
