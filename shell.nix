let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python-pkgs: [
      python-pkgs.graphviz
      python-pkgs.networkx
      python-pkgs.matplotlib
#      python-pkgs.vemvShellHook
    ]))
  ];

  shellHook = ''
    python=$(dirname $(dirname $(which python)))
    pwd=$PWD

    ln -sf "$python" ".python"
  '';
}
