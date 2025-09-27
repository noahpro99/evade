{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-25.05";
  };
  outputs =
    { nixpkgs, ... }:

    let
      pkgs = import nixpkgs {
        system = "x86_64-linux";
        config.allowUnfree = true;
      };
    in
    {
      devShells."x86_64-linux".default = pkgs.mkShell {
        LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
          pkgs.stdenv.cc.cc
          "/run/opengl-driver"
        ];

        venvDir = ".venv";
        packages = with pkgs; [
          (python313.withPackages (
            ps: with ps; [
              venvShellHook
              pip
              numpy
            ]
          ))
          bashInteractive
          uv
        ];
      };
    };
}
