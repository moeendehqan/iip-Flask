FROM balenalib/raspberry-pi-debian-python


WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx
# Install PyTorch directly
RUN pip install torch torchvision torchaudio -f https://download.pytorch.org/whl/cpu/torch_stable.html
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

CMD ["python", "run.py"]
