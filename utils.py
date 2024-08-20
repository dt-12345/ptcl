import struct
import typing

def align(pos: int, align: int) -> int:
    return (pos + align - 1) & -align

class ReadableWriteableStream:
    __slots__ = ["stream"]

    def __init__(self, stream: typing.BinaryIO):
        self.stream: typing.BinaryIO = stream

    def seek(self, pos: int) -> None:
        self.stream.seek(pos)

    def skip(self, n: int) -> None:
        self.stream.seek(self.stream.tell() + n)
    
    def tell(self) -> int:
        return self.stream.tell()
    
    def align(self, align: int) -> None:
        self.seek(align(self.tell(), align))

    def write(self, b: bytes) -> None:
        self.stream.write(b)

    def read(self, *args) -> bytes:
        return self.stream.read(*args)

    def read_u8(self) -> int:
        return struct.unpack("B", self.read(1))[0]

    def read_u16(self) -> int:
        return struct.unpack("<H", self.read(2))[0]

    def read_u32(self) -> int:
        return struct.unpack("<I", self.read(4))[0]
    
    def read_s8(self) -> int:
        return struct.unpack("b", self.read(1))[0]

    def read_s16(self) -> int:
        return struct.unpack("<h", self.read(2))[0]

    def read_s32(self) -> int:
        return struct.unpack("<i", self.read(4))[0]
    
    def read_f32(self) -> float:
        return struct.unpack("<f", self.read(4))[0]
    
    def read_color(self) -> typing.Tuple[float, float, float, float]:
        return struct.unpack("<ffff", self.read(16))
    
    def read_string(self, max_len: int = -1) -> str:
        result: bytes = b''
        cur_char: bytes = self.read(1)
        while cur_char != b'\x00':
            if max_len != -1 and len(result) > max_len:
                break
            result += cur_char
            cur_char = self.read(1)
        return result.decode("utf-8")
    
class SeekContext:
    def __init__(self, stream: ReadableWriteableStream, offset: int = -1):
        self._stream = stream
        self._offset = offset
        self._jumpack = stream.tell()

    def __enter__(self):
        if self._offset != -1:
            self._stream.seek(self._offset)
        return self._offset
    
    def __exit__(self, *args):
        self._stream.seek(self._jumpack)

class RelativeSeekContext(SeekContext):
    def __init__(self, stream: ReadableWriteableStream, offset: int):
        super().__init__(stream, offset + stream.tell())