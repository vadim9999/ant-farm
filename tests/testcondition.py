from threading import Condition
import io

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            print("buffer start with \..")
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

def main():
    output = StreamingOutput()
    # b'\xff\xd8'
    print(output.write(b'\xff\xd8df0'))
    # output.write(b'\xff\xd8df')
    with output.condition:
        output.condition.wait()
        frame = output.frame
    print("Continue execute")
if __name__ == '__main__':
    main()
