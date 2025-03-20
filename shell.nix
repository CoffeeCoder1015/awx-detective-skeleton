{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [ pkgs.python3 pkgs.uv pkgs.virtualenv ];

  shellHook = ''
    # Create virtual environment if it doesn't exist
    if [ ! -d ".venv" ]; then
      virtualenv .venv
    fi

    # Activate virtual environment
    source .venv/bin/activate

    # Ensure uv is installed in the venv
    uv venv recreate --python $(which python3)
    uv pip install --upgrade uv
    echo "Virtual environment ready with uv installed."
  '';
}
