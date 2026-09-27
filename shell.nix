{pkgs ? import <nixpkgs> {} } :
pkgs.mkShell {
    packages = [
        (pkgs.python314.withPackages(pypkgs: with pypkgs; [
            numpy
            pygame
            pillow
            requests
        ]))
    ];
    shellHook = ''
        echo "Stored API key in key.txt into variable MOTH_API_KEY"
        export MOTH_API_KEY="$(cat ./key.txt)"
    '';

}
