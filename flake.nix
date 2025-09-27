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
      venvDir = ".venv";
    in
    {
      devShells."x86_64-linux".default = pkgs.mkShell {
        LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
          pkgs.stdenv.cc.cc
          pkgs.libGL
          pkgs.glib
          pkgs.openssl
          "/run/opengl-driver"
        ];
        venvDir = venvDir;
        packages = with pkgs; [
          (python312.withPackages (
            ps: with ps; [
              venvShellHook
              pip
              numpy
              requests
            ]
          ))
          bashInteractive
          grim
          uv
        ];
        shellHook = ''
          export SSL_CERT_FILE=${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt
          export REQUESTS_CA_BUNDLE=${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt
        '';
      };
    };
}
