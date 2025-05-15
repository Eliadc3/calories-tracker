{ pkgs }: {
  deps = [
    pkgs.python3Full
    pkgs.python3Packages.pip
    pkgs.python3Packages.setuptools
    pkgs.python3Packages.wheel
    pkgs.python3Packages.gspread
    pkgs.python3Packages.oauth2client
    pkgs.python3Packages.pandas
    pkgs.python3Packages.flask
  ];
}

