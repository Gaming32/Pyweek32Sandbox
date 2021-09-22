# pyright: reportWildcardImportFromLibrary=false
import pygame
from pw32.client import globals
from pw32.utils import autoslots
from pw32.world import BlockTypes, WorldChunk
from pygame import *
from pygame.locals import *

BLOCK_RENDER_SIZE = 75
CHUNK_RENDER_SIZE = BLOCK_RENDER_SIZE * 16


@autoslots
class ClientWorld:
    loaded_chunks: dict[tuple[int, int], 'ClientChunk']
    camera: Vector2

    def __init__(self) -> None:
        self.loaded_chunks = {}
        self.camera = Vector2(0, -48)
        # self.camera = Vector2()
    
    def load(self) -> None:
        pass
    
    def unload(self) -> None:
        self.loaded_chunks.clear()

    def render(self, surf: Surface) -> None:
        surf.fill((178, 255, 255)) # Sky blue
        render_chunks = self.loaded_chunks.copy()
        half_size = Vector2(surf.get_size()) / 2
        for ((cx, cy), chunk) in render_chunks.items():
            chunk_render = chunk.render()
            rpos = (Vector2(cx, cy) * 16 - self.camera) * BLOCK_RENDER_SIZE
            rpos += half_size
            rpos.y = surf.get_height() - rpos.y
            surf.blit(chunk_render, chunk_render.get_rect().move(rpos))
        self.dirty = len(self.loaded_chunks) != len(render_chunks)


@autoslots
class ClientChunk:
    chunk: WorldChunk
    dirty: bool
    surf: Surface

    def __init__(self, chunk: WorldChunk) -> None:
        self.chunk = chunk
        self.dirty = True
        self.surf = Surface((CHUNK_RENDER_SIZE, CHUNK_RENDER_SIZE)).convert_alpha() # type: ignore
    
    def render(self) -> Surface:
        if self.dirty:
           self.surf.fill((0, 0, 0, 0))
           for x in range(16):
                for y in range(16):
                    block = self.chunk.get_tile_type(x, y)
                    if block == BlockTypes.AIR:
                        continue
                    elif block == BlockTypes.DIRT:
                        color = (155, 118, 83) # Dirt color
                    elif block == BlockTypes.GRASS:
                        color = (65, 152, 10) # Grass color
                    elif block == BlockTypes.STONE:
                        color = (119, 119, 119) # Stone color
                    rpos = Vector2(x, 15 - y) * BLOCK_RENDER_SIZE
                    self.surf.fill(color, Rect(rpos, (BLOCK_RENDER_SIZE, BLOCK_RENDER_SIZE)))
           self.dirty = False
        return self.surf 
