# Invariant Client Container

This container provides the Invariant CLI, a tool for analyzing network configuration files and policies.

## Usage

The container is configured with an entrypoint of `invariant`, so you can pass arguments to the CLI directly.

### Running Basic Commands

```bash
docker run -it --rm \
  invarianttech/client:latest \
  --help
```

## Authentication

There are two ways to authenticate the client running in the container.

### 1. Interactive Login

You can log in interactively. The CLI will provide a URL to open in your browser.

> :memo: **Note:** If you’ve never run Invariant before, the file `.local/share/invariantcli.token.cache` will not exist on your host. When Docker attempts to mount a file that doesn’t exist, it treats it as a directory. To avoid this, run `touch .local/share/invariantcli.token.cache` once to create the file. After the file is created, you won’t need to run `touch` again.

```bash
# Needed for the first run only - see note above
touch "${HOME}/.local/share/invariantcli.token.cache"
docker run -it --rm \
  -v "${HOME}/.local/share/invariantcli.token.cache:/root/.local/share/invariantcli.token.cache" \
  invarianttech/client:latest \
  login
```

*Note: Mounting a volume for credential storage (as shown above) allows you to persist your session between container runs.*

### 2. Environment Variables

For CI/CD or non-interactive use, you can provide authentication details via environment variables:

```bash
docker run -it --rm \
  -v "$(pwd):/data" \
  -e INVARIANT_API_TOKEN \
  -e INVARIANT_ORGANIZATION_NAME \
  invarianttech/client:latest  \
  run
```

### Analyzing Local Files

To analyze files in your current directory, mount it to `/data` inside the container:

```bash
docker run -it --rm \
  -v "$(pwd):/data" \
  -v "${HOME}/.local/share/invariantcli.token.cache:/root/.local/share/invariantcli.token.cache" \
  invarianttech/client:latest  \
  run
```

### Shell Function
You can use this shell function in your shell configuration to allow for easy invocation.

```bash
function invariant() {
    local CRED_DIR="$HOME/.local/share"
    local CRED_FILE="$CRED_DIR/invariantcli.token.cache"

    if [ ! -d "$CRED_DIR" ]; then
        mkdir -p "$CRED_DIR"
    fi

    if [ ! -f "$CRED_FILE" ]; then
        touch "$CRED_FILE"
    fi

    chmod 0600 "$CRED_FILE"

    docker run \
        -it \
        --rm \
        --user "$(id -u):$(id -g)" \
        -v "$(pwd):/data" \
        -v "$CRED_FILE:/creds" \
        invariant-tech/invariant "$@"
}
```

Afterwards command invocation becomes simply
```bash
$ invariant --help
usage: invariant [-h] [--version] {login,eval,run,sync,fetch,show,snapshots,networks,version,rules,definitions,locations} ...

Invariant analyzes network snapshots

options:
  -h, --help            show this help message and exit
  --version             Display the client and server version.

available commands:
  Run [command] --help for more information.

  {login,eval,run,sync,fetch,show,snapshots,networks,version,rules,definitions,locations}
    login               Authenticate by opening a link in your browser.
    eval                Test a single access policy rule.
    run                 Analyze the current snapshot.
    sync                Update the target Invariant network from remote sources.
    fetch               Fetch network configs from remote sources to disk.
    show                Access network snapshot analysis results.
    snapshots           List or manage your network snapshots.
    networks            List or manage networks.
    version             Display the client and server versions.
    rules               List or manage rules.
    definitions         List or manage definitions.
    locations           List or manage locations.
```