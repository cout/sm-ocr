This is how I do it:

```
sudo apt-get install \
  python3-venv python3-dev \
  tesseract libtesseract-dev \
  pkg-config \
  libavformat-dev libavcodec-dev libavdevice-dev libavutil-dev \
  libavfilter-dev libswscale-dev libswresample-dev

python3 -m venv env
. env/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```
