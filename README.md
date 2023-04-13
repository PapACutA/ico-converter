# ico-converter
ico-converter is a simple tool to generate ico files from images. A given Image will be put into a square format and centered within this format without distorting it. Than it will be resized to resolutions needed for an icon. The conversion itself is done by the Python Image Library (PIL).

## generating an executable with pyinstaller
to generate the executable i used the following command

`pyinstaller --clean --onefile --name ico-converter --windowed --add-binary="converter.ico;." --icon="converter.ico" "ico-converter.py" `