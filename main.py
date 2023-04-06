import serial
from pyllamacpp.model import Model
model = Model(ggml_model='./out.bin', n_ctx=512)
class client:
    def __init__(self, s):
        self.s = s
    def write(self, text):
        text = text + "\n\r"
        self.s.write(text.encode())
    def clear(self):
        self.s.write(b'"\x1b[2"')

s = serial.Serial('COM4')
c = client(s)
write = True
while True:
    print("START\n")
    while write:
        sr = s.read()
        print(sr.decode(), end="")
        s.write(sr)
        if sr.decode().endswith("^"):
            prompt = s.readline()
            s.write(b"\n\r")
            break
    f = prompt.decode().replace("^", "")
    print(f)
    generated_text = model.generate(f, n_predict=100)
    print(generated_text)
    c.write(generated_text)
    n = True
    while n:
        sr = s.read()
        if sr.decode()== "\n":
            n = False
