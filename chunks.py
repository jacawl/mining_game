from block import *

class Chunk:
    def __init__(self,my_chunk, left_chunk = None, right_chunk = None, above_chunk = None, below_chunk = None, y_coords = 0):
        self.map = my_chunk
        self.left_chunk = left_chunk
        self.right_chunk = right_chunk
        self.above_chunk = above_chunk
        self.below_chunk = below_chunk
        self.y_coords = y_coords

    def setAboveChunk(self, Chunk):
        self.above_chunk = Chunk
    
    def setBelowChunk(self, Chunk):
        self.below_chunk = Chunk

    def updateChunk(self, chunk):
        self.map = chunk
