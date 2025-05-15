{ pkgs }: {
  deps = [
    pkgs.python311Full
    pkgs.python311Packages.flask
    pkgs.python311Packages.pandas
  ];
}
