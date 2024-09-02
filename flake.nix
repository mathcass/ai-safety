{
  description = "Basic Python development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        pythonPackages = ps:
          with ps; [
            jupyter
            jupyterlab
            # Add other Python packages you need here
          ];

        python312 = pkgs.python312.withPackages pythonPackages;
      in {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            poetry
            python312
            stdenv.cc.cc.lib # This provides libstdc++
          ];

          shellHook = ''
            export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH
            export PYTHON_312="${python312}/bin/python"

            # Prefer Nix-provided libraries
            export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [
              pkgs.stdenv.cc.cc
              pkgs.zlib
              pkgs.glib
            ]}:$LD_LIBRARY_PATH
          '';
        };
      });
}
